#!/usr/bin/env python3
# encoding=utf8

import profile
import sys
import json
import os

from arg_utils import ArgUtils
from iterm2_session_support import Iterm2SessionSupport
from expect_param_support import ExpectParamSupport
WORK_PATH = os.path.dirname(sys.argv[0])
workNodes = []


def main():
    global workNodes
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
            (workNodes, ids) = getNodes(sessions, nodeIds)

        if ids:
            print("\n {} Cannot find the node [{}]\n".format(getRedContent("✗"), getRedContent(",".join(ids))))
            return
        if workNodes:
            if len(workNodes) == 1:
                # 单个tab
                # 默认     在当前tab打开
                # -t      在新tab打开
                # -w      在新窗口打开
                support = Iterm2SessionSupport(WORK_PATH)
                if ArgUtils.inNewTab():
                    support.open(workNodes, True, False)
                    return
                if ArgUtils.inNewWindow():
                    support.open(workNodes, False, True)
                    return
                # 在当前tab中执行
                os.system(ExpectParamSupport.getCmd(workNodes[0]))
            else:
                # 多个tab
                # 默认/-t  在当前窗口，新开多个tab打开
                # -w      在新窗口，新开多个tab打开        
                support = Iterm2SessionSupport(WORK_PATH)
                support.open(workNodes, False, True)
                return


            '''
            for node in workNodes:
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
