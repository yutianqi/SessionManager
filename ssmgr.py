#!/usr/bin/env python3
# encoding=utf8

import json
import iterm2

from platform import node

from arg_utils import ArgUtils

nodes = []


def main():
    global nodes
    workMode = ArgUtils.getWorkMode()
    sessions = loadSessions()

    if "ls" == workMode:
        targetSessions = sessions

        # ssmgr -m ls -n 6        显示指定节点下的节点列表
        if ArgUtils.getNodeId() != -1:
            # print("expect Id=" + str(ArgUtils.getNodeId()))
            node = getNode(sessions, ArgUtils.getNodeId())
            # print(node)
            targetSessions = [node]

        # ssls -v          包含节点IP信息
        funcName = getContent
        if ArgUtils.isDetail():
            funcName = getDetailContent

        # ssls -l <n>      展开到第n层
        # ssls -a          平铺展示

        treePrint(targetSessions, "", funcName)

    if "manage" == workMode:
        pass

    if "open" == workMode:
        if ArgUtils.getNodeId() != -1:
            # print("expect Id=" + str(ArgUtils.getNodeId()))
            node = getNode(sessions, ArgUtils.getNodeId())
            # print(node)
            nodes = [
                {
                    "nodeName": "L4-Master0_240",
                    "nodeType": "session",
                    "nodeId": "43",
                    "ip": "119.3.215.153",
                    "port": "22",
                    "username": "ossuser",
                    "password": "Huawei@Cloud8#"
                }
            ]
            iterm2.run_until_complete(openSession)


def getNode(nodes, id):
    for item in nodes:
        # print("->" + item.get("nodeId"))
        if item.get("nodeId") == id:
            return item
        if item.get("childNodes"):
            node = getNode(item.get("childNodes"), id)
            if node:
                return node
    return None


def loadSessions():
    with open("sessions.json") as f:
        lines = f.readlines()
        # print(lines)
        sessions = json.loads("".join(lines))
        # print(len(sessions))
        # print(len(sessions[0].get("childNodes")[0].get("childNodes")))
    return sessions

# TODO 需要提取到单独工具类


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


def getContent(node):
    return node.get('nodeId') + "> " + node.get('nodeName')


def getDetailContent(node):
    # print(node)
    if node.get('ip'):
        return getContent(node) + " " + node.get('ip')
    return getContent(node)


async def openSession(connection):
    app = await iterm2.async_get_app(connection)
    window = app.current_window
    if window is not None:
        for item in nodes:
            print("createTab" + item.get('nodeName'))
            await window.async_create_tab(profile="Copy of Default")
            session = app.current_terminal_window.current_tab.current_session
            # Change colour of tab
            change = iterm2.LocalWriteOnlyProfile()
            colour = iterm2.Color(102, 178, 255)
            change.set_tab_color(colour)
            change.set_use_tab_color(True)
            # Change colour of badge - text embedded into screen
            colour_badge = iterm2.Color(255, 255, 51, 129)
            change.set_badge_color(colour_badge)
            # Pull name from csv line and use for badge
            change.set_badge_text(item.get('nodeName'))
            await session.async_set_profile_properties(change)
            
            # Execute the command - could be telnet, ssh etc...
            # await session.async_send_text("ssh ossuser@" + item.get('ip') + "\n")
            await session.async_send_text("/Users/yutianqi/iterm2-session/jump.sh /Users/yutianqi/iterm2-session/119.3.215.153.json" + "\n")            

    else:
        await iterm2.window.Window.async_create(connection)
        window = app.current_window
        for item in nodes:
            print("createTab" + item.get('nodeName'))
            await window.async_create_tab(profile="Copy of Default")
            session = app.current_terminal_window.current_tab.current_session
            # Change colour of tab
            change = iterm2.LocalWriteOnlyProfile()
            colour = iterm2.Color(102, 178, 255)
            change.set_tab_color(colour)
            change.set_use_tab_color(True)
            # Change colour of badge - text embedded into screen
            colour_badge = iterm2.Color(255, 255, 51, 129)
            change.set_badge_color(colour_badge)
            # Pull name from csv line and use for badge
            change.set_badge_text(item.get('nodeName'))
            await session.async_set_profile_properties(change)
            
            # Execute the command - could be telnet, ssh etc...
            # await session.async_send_text("ssh ossuser@" + item.get('ip') + "\n")
            await session.async_send_text("/Users/yutianqi/iterm2-session/jump.sh /Users/yutianqi/iterm2-session/119.3.215.153.json" + "\n")            



if __name__ == "__main__":
    main()
