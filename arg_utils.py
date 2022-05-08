#!/usr/bin/env python3
# encoding=utf8

import argparse

class ArgUtils():



    parser = argparse.ArgumentParser()
    # parser.add_argument('--foo', action='store_true', help='foo help')

    subparsers = parser.add_subparsers(dest='workMode')

    subparserList = subparsers.add_parser('list', help='list help')
    subparserList.add_argument("-i", "--nodeId", default="-1", help="Specify node ID")
    subparserList.add_argument("-n", "--nodeName", default="-1", help="Specify node name")
    subparserList.add_argument("-v", action='store_true', default=False, help="Show detail info")


    subparserOpen = subparsers.add_parser('open', help='open help')
    subparserOpen.add_argument("-s", "--nodeIds", required=True, help="Specify node ID")


    subparserManage = subparsers.add_parser('add', help='manage help')
    subparserManage.add_argument('ver', help='b version help')

    subparserManage = subparsers.add_parser('del', help='manage help')
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
