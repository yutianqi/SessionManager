#!/usr/bin/env python3
# encoding=utf8

import json
from platform import node

from arg_utils import ArgUtils

def main():
    sessions = loadSessions()
    if "ls" == ArgUtils.getWorkMode():
        if ArgUtils.getNodeId():
            print("expect Id=" + str(ArgUtils.getNodeId()))
            node = getNode(sessions, ArgUtils.getNodeId()) 

        # ssls -n 6        显示指定节点下的节点列表
        # ssls -l <n>      展开到第n层
        # ssls -a          平铺展示
        # ssls -v          包含节点IP信息

        print(node)
        targetSessions = [node]

        treePrint(targetSessions, "", getContent)

    if "manage" == ArgUtils.getWorkMode():
        pass

def getNode(nodes, id):
    for item in nodes:
        print("->" + item.get("nodeId"))
        if item.get("nodeId") == id:
            return item
        if item.get("childNodes"):
            node = getNode(item.get("childNodes"), id)
            if node:
                return node
        else:
            print("check child")
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
            treePrint(node.get('childNodes'), next, getContent)


def getContent(node):
    return node.get('nodeId') + "> " + node.get('nodeName')


if __name__ == "__main__":
    main()
