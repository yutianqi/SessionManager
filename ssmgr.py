#!/usr/bin/env python3
# encoding=utf8

import profile
import sys
import json
import iterm2
import os

from arg_utils import ArgUtils

WORK_PATH = os.path.dirname(sys.argv[0])
NODES = []


def main():
    global NODES
    workMode = ArgUtils.getWorkMode()
    if not workMode:
        print("\n {} Please specify the work mode first.\n".format(getRedContent("✗")))
        return

    (total, sessions) = loadSessions()

    if "list" == workMode:
        targetSessions = sessions

        targetNode = ArgUtils.getNodeId()
        if targetNode != "-1":
            node = getNode(sessions, targetNode)
            if node:
                targetSessions = [node]
                print("")
            else:
                print("\n {} Cannot find the node [{}]\n".format(getRedContent("✗"), getRedContent(targetNode)))
                return

        if len(targetSessions) == 0:
            print("\n {} No record found...\n".format(getRedContent("✗")))
            return
        if targetNode == "-1":
            print(" {} Listing {} nodes...\n".format(getGreenContent("✔"), total))

        # sl -a                     平铺展示
        # displayFuncName = getDisplayContent
        displayFuncName = getDisplayContent
        if ArgUtils.isDetail():
            displayFuncName = getDetailDisplayContent

        # sl -l <n>                 展开到第n层
        treePrint(targetSessions, "   ", displayFuncName)
        print("")

    # ssmgr -m manage
    if "manage" == workMode:
        # sm -a <nodeName> <ip> <port> <username> <password>
        # sm -a -f <filename>
        # sm -d <nodeId>
        pass

    if "open" == workMode:
        # so -ns 47,48-50
        if ArgUtils.getNodeIds():
            nodeIds = getNodeIds(ArgUtils.getNodeIds())
            (NODES, ids) = getNodes(sessions, nodeIds)
        if ids:
            print("找不到节点：" + str(ids))
            print("\n {} Cannot find the node [{}]\n".format(getRedContent("✗"), getRedContent(",".join(ids))))
            return

        # so -ns 47,48-50 -w：新窗口打开
        # so -ns 47,48-50 -t：新标签打开

        if NODES:
            iterm2.run_until_complete(openSession)
            '''
            for node in NODES:
                print(os.path.join(WORK_PATH, "jump.exp") + " " + getParams(node) + "\n")
            '''


def getRedContent(content):
    return "\033[0;31;m{}\033[0m".format(content)


def getGreenContent(content):
    return "\033[0;32;m{}\033[0m".format(content)


def getYellowContent(content):
    return "\033[0;33;m{}\033[0m".format(content)


def getNodes(sessions, ids):
    nodes = []
    for item in sessions:
        # print(item.get("nodeId"))
        if item.get("nodeId") in ids:
            nodes.append(item)
            ids.remove(item.get("nodeId"))
            if not ids:
                return (nodes, ids)
        if item.get("childNodes"):
            (subNodes, ids) = getNodes(item.get("childNodes"), ids)
            if subNodes:
                nodes.extend(subNodes)
    return (nodes, ids)


def getNode(sessions, id):
    nodes = getNodes(sessions, [id])[0]
    if nodes:
        return nodes[0]
    return None


def getParams(node):
    (nodesCounter, params) = getParamsFromNode(node)
    params.insert(0, str(nodesCounter))
    params.insert(1, "1")
    return " ".join(params)


def getParamsFromNode(node):
    levels = 1
    params = [
        "ssh",
        node.get("username"),
        node.get("ip"),
        node.get("port"),
        "0",
        "1",
        "1",
        node.get("password")
    ]
    if node.get("commands"):
        commands = ['"' + item + '"' for item in node.get("commands")]
        params.append(str(len(commands)))
        params.extend(commands)
    else:
        params.append("0")
    params.append("0")

    if node.get("jumper"):
        (subLevels, subParams) = getParamsFromNode(node.get("jumper"))
        levels += subLevels
        params.extend(subParams)
    return (levels, params)


def loadSessions():
    with open(os.path.join(WORK_PATH, "sessions.json")) as f:
        lines = f.readlines()
        sessions = json.loads("".join(lines))
    return (sessions.get("total"), sessions.get("nodes"))


def treePrint(nodes, prefix, func):
    l = len(nodes)
    for i in range(l):
        current = prefix
        next = prefix
        node = nodes[i]
        if i == l - 1:
            current += "└── " + func(node)
            next += "    "
        else:
            current += "├── " + func(node)
            next += "│   "
        print(current)

        if node.get('childNodes'):
            treePrint(node.get('childNodes'), next, func)


def getDisplayContent(node):
    return getGreenContent(node.get('nodeId')) + " → " + node.get('nodeName')


def getDetailDisplayContent(node):
    # print(node)
    if node.get('ip'):
        return getDisplayContent(node) + " " + node.get('ip')
    return getDisplayContent(node)


async def openSession(connection):
    app = await iterm2.async_get_app(connection)
    window = app.current_window

    # if not window:
    if True:
        await iterm2.window.Window.async_create(connection)
        window = app.current_window

    firstSession = True
    for item in NODES:
        if not firstSession:
            await window.async_create_tab()
            # await window.async_create_tab(profile="Copy of Default")
        else:
            firstSession = False
        session = app.current_terminal_window.current_tab.current_session
        profile = iterm2.LocalWriteOnlyProfile()

        # Change colour of tab
        # colour = iterm2.Color(102, 178, 255)
        # change.set_tab_color(colour)
        # change.set_use_tab_color(True)

        # Change colour of badge - text embedded into screen
        # Pull name from csv line and use for badge
        colour_badge = iterm2.Color(255, 255, 51, 129)
        profile.set_badge_color(colour_badge)
        profile.set_badge_text(item.get('nodeName'))

        await session.async_set_profile_properties(profile)

        # Execute the command - could be telnet, ssh etc...
        # await session.async_send_text("ssh ossuser@" + item.get('ip') + "\n")
        await session.async_send_text("expect " + os.path.join(WORK_PATH, "jump.exp") + " " + getParams(item) + "\n")


def getNodeIds(idStr):
    nodeIds = []
    for item in idStr.split(","):
        if '-' in item:
            begin = int(item.split("-")[0])
            end = int(item.split("-")[1]) + 1
            nodeIds.extend([str(i) for i in range(begin, end)])
        else:
            nodeIds.append(item)
    return nodeIds


if __name__ == "__main__":
    main()
    # print(getNodeIds("47,48-50"))
