#!/usr/bin/env python3
# encoding=utf8

from utils.arg_utils import ArgUtils
from utils.color_utils import ColorUtils

from support.session_support import SessionSupport

class SessionDeleter():

    @classmethod
    def execute(cls):
        """
        删除session功能入口
        """
        nodeIds = ArgUtils.getNodeIds()
        deletedNodeIds = SessionSupport.deleteSessions(nodeIds)
        if deletedNodeIds:
            print("\n {} Delete sessions [{}]\n".format(
                ColorUtils.getGreenContent("✔"), ColorUtils.getGreenContent(",".join([str(item) for item in deletedNodeIds]))))
        else:
            print("\n {} No session deleted\n".format(
                ColorUtils.getRedContent("✗")))
