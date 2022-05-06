#!/usr/bin/env python3
# encoding=utf8

import argparse

# from domain.work_mode import WorkMode

class ArgUtils():
    parser = argparse.ArgumentParser(description="")

    # group = parser.add_mutually_exclusive_group(required=True)
    # parser.add_argument("-n", "--nodeId", type=int)
    parser.add_argument("-n", "--nodeId")
    parser.add_argument("-m", "--mode", default="open", choices=['ls', 'manage', 'open'], help="work mode")

    # parser.add_argument("-o", "--only", action='store_true', default=False, help="only run once")

    '''
    parser.add_argument("-o", "--only", action='store_true', default=False, help="only run once")

    parser.add_argument("-f", "--force", action='store_true', default=False, help="force run")

    parser.add_argument("-d", "--db", help="db file name")
    '''

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
    def isOnlyOnce(cls):
        return cls.args.only


    @classmethod
    def isForceRun(cls):
        return cls.args.force