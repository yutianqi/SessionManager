#!/usr/bin/env python3
# encoding=utf8

# Name:         ssmgr.py
# Purpose:      Management sessions
# Author:       Yu Tianqi <ytq0415@gmail.com>
# Created:      2022.05.05 00:20:37
# Version:      0.9.3

import sys
import os

from utils.arg_utils import ArgUtils
from utils.color_utils import ColorUtils

from operation.adder import SessionAdder
from operation.deleter import SessionDeleter
from operation.opener import SessionOpener
from operation.lister import SessionLister

WORK_PATH = os.path.dirname(sys.argv[0])
VERSION = "0.9.2"


def main():
    """
    入口方法
    """
    workMode = ArgUtils.getWorkMode()
    if "add" == workMode:
        SessionAdder.execute()
        return
    if "delete" == workMode:
        SessionDeleter.execute()
        return
    if "open" == workMode:
        SessionOpener.execute()
        return
    if "list" == workMode:
        SessionLister.execute()
        return
    if ArgUtils.isShowVersion():
        print("\nSessionManager version: {}".format(VERSION))
    else:
        print("\n {} Please specify the work mode first.\n".format(
            ColorUtils.getRedContent("✗")))
    return


if __name__ == "__main__":
    main()
