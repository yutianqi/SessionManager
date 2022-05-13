#!/usr/bin/env python3
# encoding=utf8

# Name:         ssmgr.py
# Purpose:      Management sessions
# Author:       Yu Tianqi <ytq0415@gmail.com>
# Created:      2022.05.05 00:20:37
# Version:      0.9.1

import sys
import os
import json

from arg_utils import ArgUtils
from color_utils import ColorUtils
from expect_param_support import ExpectParamSupport
from session_file_utils import SessionFileUtils

WORK_PATH = os.path.dirname(sys.argv[0])
VERSION = "0.9.1"

def main():
    workMode = ArgUtils.getWorkMode()
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
    if ArgUtils.isShowVersion():
        print("\nSessionManager version: {}".format(VERSION))
    else:
        print("\n {} Please specify the work mode first.\n".format(
            ColorUtils.getRedContent("✗")))
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
            # pass
            print(" {} Listing {} nodes...\n".format(ColorUtils.getGreenContent("✔"), total))
            

        # sl -a                     平铺展示
        displayFuncName = getDisplayContent
        if ArgUtils.isLongFormat():
            displayFuncName = getLongFormatDisplayContent

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
            targetNodeIds = parseNodeIdStr(ArgUtils.getNodeIds())
            (workNodes, ids) = getSessionNodes(sessions, targetNodeIds)
        if ids:
            print("\n {} Cannot find the node [{}]\n".format(
                ColorUtils.getRedContent("✗"), ColorUtils.getRedContent(",".join([str(item) for item in ids]))))
            return
        # 对目录节点不做处理
        # workNodes = [item for item in workNodes if item.get("nodeType") == "session"]
        # print([item.get("nodeId") for item in workNodes])


        if not workNodes:
            print("\n {} No node need to be open\n".format(ColorUtils.getRedContent("✗")))
            return
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
        openResult = support.newopen(workNodes, inNewTab, inNewWindow)

        if openResult:
            print("{} 打开{}节点成功".format(ColorUtils.getRedContent("✔"), [item.get("nodeId") for item in workNodes]))
        else:
            print("{} 打开{}节点失败".format(ColorUtils.getRedContent("✗"), [item.get("nodeId") for item in workNodes]))


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
    nodeIds = parseNodeIdStr(ArgUtils.getNodeIds())
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


def getSessionNodes(sessions, ids):
    '''从指定sessions中获取id在ids列表内的session'''
    nodes = []
    for item in sessions:
        if item.get("nodeId") in ids:
            if item.get("nodeType") == "directory":
                # 如果是目录，则将目录下所有session添加到nodes中
                nodes.extend(getSubSessionNodes(item))
            else:
                # 如果是session，则该session添加到nodes中
                nodes.extend(item)
            ids.remove(item.get("nodeId"))
            if not ids:
                return (nodes, ids)
            continue
        # 如果当前节点id不在ids中，但是包含子节点，则在自节点中继续查找
        if item.get("childNodes"):
            (subNodes, ids) = getSessionNodes(item.get("childNodes"), ids)
            if subNodes:
                nodes.extend(subNodes)
    return (nodes, ids)


def getSubSessionNodes(parentNode):
    '''查询某个节点下的所有子session节点'''
    nodes = []
    if not parentNode.get("childNodes"):
        # 如果没有子节点直接返回空列表
        return nodes
    for node in parentNode.get("childNodes"):
        # 如果子节点是session，则直接添加到nodes中
        if node.get("nodeType") == "session":
            nodes.append(node)
            continue
        # 如果子节点是目录，则继续查询该目录下的子节点
        nodes.extend(getSubSessionNodes(node))
    return nodes


def getNode(sessions, id):
    '''在sessions中查询指定id的节点'''
    for item in sessions:
        if item.get("nodeId") == id:
            return item
        if item.get("childNodes"):
            node = getNode(item.get("childNodes"), id)
            if node:
                return node
    return None


def treePrint(nodes, prefix, func):
    '''打印节点树'''
    l = len(nodes)
    for i in range(l):
        current = prefix
        next = prefix
        node = nodes[i]
        if i == l - 1:
            next += "    "
            current += "└── " + func(node, next)
        else:
            next += "│   "
            current += "├── " + func(node, next)
        print(current)

        if node.get('childNodes'):
            treePrint(node.get('childNodes'), next, func)


def getDisplayContent(node, prefix):
    if node.get("nodeType") == "directory":
        return ColorUtils.getGreenContent(node.get('nodeId')) + " → " + ColorUtils.getYellowContent(node.get('nodeName'))
    return ColorUtils.getGreenContent(node.get('nodeId')) + " → " + node.get('nodeName')


def getLongFormatDisplayContent(node, prefix):
    if node.get('nodeType') == "session":
        return getDisplayContent(node, prefix) + " " + node.get('ip')
    return getDisplayContent(node, prefix)


def getDetailDisplayContent(node, prefix):
    prefix += "     "
    if node.get('nodeType') == "session":
        return "{} \n{}{}@{}:{}".format(getDisplayContent(node, prefix), prefix, node.get('username'), node.get('ip'), node.get('port'))
    return getDisplayContent(node, prefix)


def parseNodeIdStr(idStr):
    '''解析nodeId字符串'''
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
