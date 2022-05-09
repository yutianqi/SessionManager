#!/usr/bin/env python3
# encoding=utf8

import os
import sys
import iterm2
from expect_param_support import ExpectParamSupport

class SessionSupport():
    workPath = os.path.dirname(sys.argv[0])
    nodes = []
    inNewTab = False
    inNewWindow = False

    def __init__(self, workPath): 					
        self.workPath = workPath

    def newopen(self, workNodes, inNewTab, inNewWindow):
        if len(workNodes) == 1:
            # 单个tab
            # 默认     在当前tab打开
            # -t      在新tab打开
            # -w      在新窗口打开
            if inNewTab:
                self.open(workNodes, True, False)
                return
            if inNewWindow:
                self.open(workNodes, False, True)
                return
        else:
            # 多个tab
            # 默认/-t  在当前窗口，新开多个tab打开
            # -w      在新窗口，新开多个tab打开
            if inNewTab:
                self.open(workNodes, True, False)
            else:
                self.open(workNodes, False, True)
            return
        '''
        for node in workNodes:
            print(os.path.join(WORK_PATH, "jump.exp") + " " + getParams(node) + "\n")
        '''

    def open(self, nodes, inNewTab, inNewWindow):
        self.nodes = nodes
        self.inNewTab = inNewTab
        self.inNewWindow = inNewWindow
        iterm2.run_until_complete(self.openSessions)

    async def openSessions(self, connection):
        app = await iterm2.async_get_app(connection)
        window = app.current_window

        firstSession = True

        if self.inNewWindow:
            # 在新窗口中开一堆窗口
            await iterm2.window.Window.async_create(connection)
            window = app.current_window
            for item in self.nodes:
                if not firstSession:
                    await window.async_create_tab()
                else:
                    firstSession = False
                await self.openSession(app.current_terminal_window.current_tab.current_session, item)
        else:
            # 在新Tab中开一堆窗口
            for item in self.nodes:
                await window.async_create_tab()
                await self.openSession(app.current_terminal_window.current_tab.current_session, item)

    async def openSession(self, session, item):
        profile = iterm2.LocalWriteOnlyProfile()
        # Change colour of tab
        # colour = iterm2.Color(102, 178, 255)
        # change.set_tab_color(colour)
        # change.set_use_tab_color(True)

        # Change colour of badge - text embedded into screen
        # Pull name from csv line and use for badge
        colour_badge = iterm2.Color(255, 255, 51, 129)
        profile.set_badge_color(colour_badge)
        profile.set_badge_text(item.get('nodeName'))

        await session.async_set_profile_properties(profile)

        # Execute the command - could be telnet, ssh etc...
        # await session.async_send_text("ssh ossuser@" + item.get('ip') + "\n")
        await session.async_send_text(ExpectParamSupport.getCmd(item))


