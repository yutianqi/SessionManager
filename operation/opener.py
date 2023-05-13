#!/usr/bin/env python3
# encoding=utf8

import os

from utils.arg_utils import ArgUtils
from utils.color_utils import ColorUtils

from support.session_support import SessionSupport
from support.py_param_support import PyParamSupport
from support.native_session_support import NativeSessionSupport
from support.iterm2_session_support import Iterm2SessionSupport

class SessionOpener():

    def execute():
        """
        打开session功能入口
        """
        workNodes = []
        # so -ns 47,48-50
        if ArgUtils.getNodeIds():
            targetNodeIds = ArgUtils.getNodeIds()
            # print("targetNodeIds={}".format(targetNodeIds))
            (workNodes, ids) = SessionSupport.getNodes(nodeIds=targetNodeIds)
        if ids:
            print("\n {} Cannot find the node [{}]\n".format(
                ColorUtils.getRedContent("✗"), ColorUtils.getRedContent(",".join([str(item) for item in ids]))))
            return
        # 对目录节点不做处理
        # workNodes = [item for item in workNodes if item.get("nodeType") == "session"]
        # print([item.get("nodeId") for item in workNodes])

        # print(workNodes)
        if not workNodes:
            print("\n {} No node need to be open\n".format(
                ColorUtils.getRedContent("✗")))
            return
        inNewTab = ArgUtils.inNewTab()
        inNewWindow = ArgUtils.inNewWindow()

        # print("workNodes=" + str(workNodes))
        # print("inNewTab=" + str(inNewTab))
        # print("inNewWindow=" + str(inNewWindow))
        # 在当前tab中打开一个session
        if len(workNodes) == 1 and not inNewTab and not inNewWindow:
            # cmd = ExpectParamSupport.getCmd(workNodes[0])
            cmd = PyParamSupport.getCmd(workNodes[0])
            # print(cmd)
            os.system(cmd)
            return
        # 需要在新tab/window打开session场景，根据实际情况选择App支持
        support = NativeSessionSupport(WORK_PATH)
        app = ArgUtils.getApp()
        if app == "iterm2":
            support = Iterm2SessionSupport(WORK_PATH)
        
        openResult = support.newopen(workNodes, inNewTab, inNewWindow)

        if openResult:
            print("{} 打开{}节点成功".format(ColorUtils.getGreenContent(
                "✔"), [item.get("nodeId") for item in workNodes]))
        else:
            print("{} 打开{}节点失败".format(ColorUtils.getRedContent(
                "✗"), [item.get("nodeId") for item in workNodes]))


