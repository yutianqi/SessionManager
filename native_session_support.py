#!/usr/bin/env python3
# encoding=utf8

import os
import sys

class SessionSupport():
    workPath = os.path.dirname(sys.argv[0])
    nodes = []
    iterm2 = None
    inNewTab = False
    inNewWindow = False

    def __init__(self, workPath): 					
        self.workPath = workPath

    def newopen(self, workNodes, inNewTab, inNewWindow):
        print("Operation not support for now...")