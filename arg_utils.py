#!/usr/bin/env python3
# encoding=utf8

import argparse

class ArgUtils():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='workMode')

    subparserList = subparsers.add_parser('list', help='list help')
    subparserList.add_argument("-i", "--nodeId", default="-1", help="Specify node ID")
    subparserList.add_argument("-n", "--nodeName", default="-1", help="Specify node name")
    subparserList.add_argument("-v", action='store_true', default=False, help="Show detail info")


    subparserOpen = subparsers.add_parser('open', help='open help')
    subparserOpen.add_argument("-s", "--nodeIds", required=True, help="Specify node ID")
    subparserOpen.add_argument("-t", "--tab", action='store_true', default=False, required=False, help="")
    subparserOpen.add_argument("-w", "--window", action='store_true', default=False, required=False, help="")
    subparserOpen.add_argument("-a", "--app", default="native", required=False, help="")


    subparserManage = subparsers.add_parser('add', help='add help')
    subparserManage.add_argument('ver', help='b version help')


    subparserManage = subparsers.add_parser('del', help='del help')
    subparserManage.add_argument('ver', help='b version help')
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