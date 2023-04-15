#!/usr/bin/env python3
# encoding=utf8

from utils.arg_utils import ArgUtils
from utils.color_utils import ColorUtils

from support.session_support import SessionSupport

class SessionLister():

    @classmethod
    def execute(cls):
        """
        展示session列表功能入口
        """
        targetNodeIds = ArgUtils.getNodeIds()

        # print("targetNodeIds=" + str(targetNodeIds))

        if not targetNodeIds:
            (sessions, ids) = targetSessions = SessionSupport.getNodes()
            targetSessions = sessions
        else:
            targetNodeId = targetNodeIds[0]
            targetSessions = [SessionSupport.getNode(sessions=[], nodeId=targetNodeId)]
        if not targetSessions:
            if targetNodeIds:
                print("\n {} Cannot find the node {}\n".format(
                    ColorUtils.getRedContent("✗"), ColorUtils.getRedContent(targetNodeIds)))
                return
            else:
                print("\n {} No record found...\n".format(
                    ColorUtils.getRedContent("✗")))
                return
        print(" {} Listing {} nodes...\n".format(
            ColorUtils.getGreenContent("✔"), len(targetSessions)))

        # sl -a                     平铺展示
        displayFuncName = cls.getDetailDisplayContent
        if ArgUtils.isLongFormat():
            displayFuncName = cls.getLongFormatDisplayContent

        # if ArgUtils.isDetail():
        #     displayFuncName = getDetailDisplayContent

        # print(targetSessions)
        cls.treePrint(targetSessions, "   ", displayFuncName)


    @classmethod
    def treePrint(cls, nodes, prefix, func):
        """
        打印节点树

        :param nodes: 节点列表
        :param prefix: 显示前缀
        :param func: 获取节点显示内容的方法
        """
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
                cls.treePrint(node.get('childNodes'), next, func)

    @classmethod
    def getDisplayContent(cls, node, prefix):
        """
        获取节点显示内容

        :param node: 节点
        :param prefix: 前缀
        :returns: 节点详情显示内容
        """    
        if node.get("nodeType") == "directory":
            return ColorUtils.getGreenContent(node.get('nodeId')) + " → " + ColorUtils.getYellowContent(node.get('nodeName'))
        return ColorUtils.getGreenContent(node.get('nodeId')) + " → " + node.get('nodeName')

    @classmethod
    def getLongFormatDisplayContent(cls, node, prefix):
        """
        获取节点显示内容(长格式)

        :param node: 节点
        :param prefix: 前缀
        :returns: 节点详情显示内容
        """
        if node.get('nodeType') == "session":
            # return getDisplayContent(node, prefix) + " " + node.get('ip')
            return "{} {}@{}:{}".format(cls.getDisplayContent(node, prefix), node.get('username'), node.get('ip'), node.get('port'))
        return cls.getDisplayContent(node, prefix)

    @classmethod
    def getDetailDisplayContent(cls, node, prefix):
        """
        获取节点显示内容(详情)

        :param node: 节点
        :param prefix: 前缀
        :returns: 节点详情显示内容
        """
        prefix += "     "
        if node.get('nodeType') == "session":
            return "{} \n{}{}@{}:{}".format(cls.getDisplayContent(node, prefix), prefix, node.get('username'), node.get('ip'), node.get('port'))
        return cls.getDisplayContent(node, prefix)


