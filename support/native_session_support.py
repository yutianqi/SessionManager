#!/usr/bin/env python3
# encoding=utf8

import os
import sys
from utils.color_utils import ColorUtils

class NativeSessionSupport():
    workPath = os.path.dirname(sys.argv[0])
    nodes = []
    iterm2 = None
    inNewTab = False
    inNewWindow = False

    def __init__(self, workPath): 					
        self.workPath = workPath

    def newopen(self, workNodes, inNewTab, inNewWindow):
        # print("\n {} Open sessions in new tab/window not support for [{}] currently.".format(ColorUtils.getRedContent("✗"), "Native"))
        print("\n * Open sessions in new tab/window not support for [Native] currently.")
        print(" * Please open new tab/window manualy or use the -a param to specify a terminal app, e.g. [-a iterm2].\n")
        return False

