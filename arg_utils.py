#!/usr/bin/env python3
# encoding=utf8

import argparse

# from domain.work_mode import WorkMode


class ArgUtils():
    parser = argparse.ArgumentParser(description="")

    # group = parser.add_mutually_exclusive_group(required=True)
    # parser.add_argument("-n", "--nodeId", type=int)
    parser.add_argument("-n", "--nodeId")
    parser.add_argument("-s", "--nodeIds", default="")
    parser.add_argument("-m", "--mode", default="open",
                        choices=['ls', 'manage', 'open'], help="work mode")
    parser.add_argument("-v", action='store_true',
                        default=False, help="detail")

    args = parser.parse_args()

    @classmethod
    def getWorkMode(cls):
        return cls.args.mode

    @classmethod
    def getNodeId(cls):
        if cls.args.nodeId:
            return cls.args.nodeId
        return -1

    @classmethod
    def getNodeIds(cls):
        return cls.args.nodeIds

    @classmethod
    def isDetail(cls):
        return cls.args.v
