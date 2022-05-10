#!/usr/bin/env python3
# encoding=utf8

import sys
import os
import json

from arg_utils import ArgUtils
from color_utils import ColorUtils
from expect_param_support import ExpectParamSupport
from session_file_utils import SessionFileUtils

WORK_PATH = os.path.dirname(sys.argv[0])

def main():
    workMode = ArgUtils.getWorkMode()
    if not workMode:
        print("\n {} Please specify the work mode first.\n".format(
            ColorUtils.getRedContent("✗")))
        return
    if "list" == workMode:
        listSessions()
        return
    if "open" == workMode:
        openSessions() 
        return
    if "add" == workMode:
        addSessions()
        return
    if "delete" == workMode:
        deleteSessions()
        return


def listSessions():
        (total, sessions) = SessionFileUtils.loadSessions()
        targetSessions = sessions

        targetNode = ArgUtils.getNodeId()
        if targetNode != -1:
            node = getNode(sessions, targetNode)
            if node:
                targetSessions = [node]
                print("")
            else:
                print("\n {} Cannot find the node [{}]\n".format(
                    ColorUtils.getRedContent("✗"), ColorUtils.getRedContent(targetNode)))
                return

        if len(targetSessions) == 0:
            print("\n {} No record found...\n".format(ColorUtils.getRedContent("✗")))
            return
        if targetNode == -1:
            print(" {} Listing {} nodes...\n".format(
                ColorUtils.getGreenContent("✔"), total))

        # sl -a                     平铺展示
        # displayFuncName = getDisplayContent
        displayFuncName = getDisplayContent
        if ArgUtils.isDetail():
            displayFuncName = getDetailDisplayContent

        # sl -l <n>                 展开到第n层
        treePrint(targetSessions, "   ", displayFuncName)
        print("")


def openSessions():
        workNodes = []
        (total, sessions) = SessionFileUtils.loadSessions()
        # so -ns 47,48-50
        if ArgUtils.getNodeIds():
            nodeIds = getNodeIds(ArgUtils.getNodeIds())
            (workNodes, ids) = getNodes(sessions, nodeIds)
        if ids:
            print("\n {} Cannot find the node [{}]\n".format(
                ColorUtils.getRedContent("✗"), ColorUtils.getRedContent(",".join([str(item) for item in ids]))))
            return
        # 对目录节点不做处理
        workNodes = [item for item in workNodes if item.get("nodeType") == "session"]
        if not workNodes:
            print("\n {} No node need to be open\n".format(ColorUtils.getRedContent("✗")))
        inNewTab = ArgUtils.inNewTab()
        inNewWindow = ArgUtils.inNewWindow()
        # 在当前tab中打开一个session
        if len(workNodes) == 1 and not inNewTab and not inNewWindow:
            os.system(ExpectParamSupport.getCmd(workNodes[0]))
            return
        # 需要在新tab/window打开session场景，根据实际情况选择App支持
        # support = Iterm2SessionSupport(WORK_PATH)
        supportModule = __import__(ArgUtils.getApp() + '_session_support')
        support = supportModule.SessionSupport(WORK_PATH)
        support.newopen(workNodes, inNewTab, inNewWindow)


def addSessions():
    if ArgUtils.getSessionContentInTextFormat():
        pass
    if ArgUtils.getSessionContentInJsonFormat():
        session = json.loads(ArgUtils.getSessionContentInJsonFormat())	
        SessionFileUtils.addSessionsInMap([session])
    if ArgUtils.getSessionContentInFileFormat():
        fileName = ArgUtils.getSessionContentInFileFormat()
        with open(fileName) as f:
            lines = f.readlines()
            data = json.loads("".join(lines))
            if type(data) == list:
                SessionFileUtils.addSessionsInMap(data)
            elif type(data) == map:
                SessionFileUtils.addSessionsInMap([data])
            else:
                print("\n {} Invalid format\n".format(ColorUtils.getRedContent("✗")))  

    if ArgUtils.getSessionContentInInteractiveMode():
        nodeName = input("session name: ")
        ip = input("ip: ")
        port = input("port: ")
        username = input("username: ")
        password = input("password: ")
        SessionFileUtils.addSession(nodeName, ip, port, username, password)

def deleteSessions():
    nodeIds = getNodeIds(ArgUtils.getNodeIds())
    deletedNodeIds = SessionFileUtils.deleteSessionsMain(nodeIds)
    if deletedNodeIds:
        print("\n {} Delete sessions [{}]\n".format(
            ColorUtils.getGreenContent("✔"), ColorUtils.getGreenContent(",".join([str(item) for item in deletedNodeIds]))))
    else:
        print("\n {} No session deleted\n".format(ColorUtils.getRedContent("✗")))


def getNodes(sessions, ids):
    nodes = []
    for item in sessions:
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
    return ColorUtils.getGreenContent(node.get('nodeId')) + " → " + node.get('nodeName')


def getDetailDisplayContent(node):
    if node.get('ip'):
        return getDisplayContent(node) + " " + node.get('ip')
    return getDisplayContent(node)


def getNodeIds(idStr):
    nodeIds = []
    for item in idStr.split(","):
        if '-' in item:
            begin = int(item.split("-")[0])
            end = int(item.split("-")[1]) + 1
            nodeIds.extend([i for i in range(begin, end)])
        else:
            nodeIds.append(int(item))
    return nodeIds


if __name__ == "__main__":
    main()
