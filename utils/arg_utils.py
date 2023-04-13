#!/usr/bin/env python3
# encoding=utf8

import argparse

class ArgUtils():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', "--version", action='store_true', default=False, help='show version')

    subparsers = parser.add_subparsers(dest='workMode')

    subparserList = subparsers.add_parser('list', help='list help')
    subparserList.add_argument("-i", "--nodeId", type=int, default=-1, help="Specify node ID")
    # subparserList.add_argument("-n", "--nodeName", default="", help="Specify node name")
    subparserList.add_argument("-l", action='store_true', default=False, help="Display in long format")
    subparserList.add_argument("-v", action='store_true', default=False, help="Show detail info")


    subparserOpen = subparsers.add_parser('open', help='open help')
    subparserOpen.add_argument("-s", "--nodeIds", required=True, help="Specify node ID")
    subparserOpen.add_argument("-t", "--tab", action='store_true', default=False, required=False, help="Open session in new tab")
    subparserOpen.add_argument("-w", "--window", action='store_true', default=False, required=False, help="Open session in new window")
    subparserOpen.add_argument("-a", "--app", default="native", required=False, help="Specify the session manage app, e.g. iterm2")


    subparserAdd = subparsers.add_parser('add', help='add help')
    # subparserAdd.add_argument("-t", "--type", default="text", choices=['text', 'json'], help="Specify the session content type")
    subparserAdd.add_argument("-t", "--text", default="", required=False, help="Add session in text format")
    subparserAdd.add_argument("-j", "--json", default="", required=False, help="Add ession in json format")
    subparserAdd.add_argument("-i", "--interactive", action='store_true', default=False, help="Add session in interactive mode")
    subparserAdd.add_argument("-f", "--file", default="", required=False, help="Add session in file format")


    subparserDelete = subparsers.add_parser('delete', help='del help')
    subparserDelete.add_argument("-s", "--nodeIds", required=True, help="Specify the ID of the node to be deleted")
    # subparserDelete.add_argument("-n", "--nodeName", default="", help="Specify the name of the node to be deleted")


    args = parser.parse_args()


    @classmethod
    def getWorkMode(cls):
        return cls.args.workMode

    @classmethod
    def getNodeId(cls):
        return cls.args.nodeId

    @classmethod
    def getNodeIds(cls):
        return cls.args.nodeIds

    @classmethod
    def isLongFormat(cls):
        return cls.args.l

    @classmethod
    def isDetail(cls):
        return cls.args.v

    @classmethod
    def inNewTab(cls):
        return cls.args.tab

    @classmethod
    def inNewWindow(cls):
        return cls.args.window
        
    @classmethod
    def getApp(cls):
        return cls.args.app

    @classmethod
    def getSessionContentInTextFormat(cls):
        return cls.args.text

    @classmethod
    def getSessionContentInJsonFormat(cls):
        return cls.args.json

    @classmethod
    def getSessionContentInInteractiveMode(cls):
        return cls.args.interactive

    @classmethod
    def getSessionContentInFileFormat(cls):
        return cls.args.file

    @classmethod
    def isShowVersion(cls):
        return cls.args.version

    @classmethod
    def parseNodeIdStr(cls, idStr):
        """
        解析nodeId字符串

        :param idStr: nodeId字符串，支持连续模式(-)和多节点模式(,)
        :returns: 节点ID列表
        """
        nodeIds = []
        for item in idStr.split(","):
            if '-' in item:
                begin = int(item.split("-")[0])
                end = int(item.split("-")[1]) + 1
                nodeIds.extend([i for i in range(begin, end)])
            else:
                nodeIds.append(int(item))
        return nodeIds
