#!/usr/bin/env python3
# encoding=utf8

import os
import sys
from expect_param_support import ExpectParamSupport

class Iterm2SessionSupport():
    workPath = os.path.dirname(sys.argv[0])
    nodes = []
    iterm2 = None
    inNewTab = False
    inNewWindow = False

    def __init__(self, workPath): 					
        self.iterm2 = __import__('iterm2')
        self.workPath = workPath

    def open(self, nodes, inNewTab, inNewWindow):
        self.nodes = nodes
        self.inNewTab = inNewTab
        self.inNewWindow = inNewWindow
        self.iterm2.run_until_complete(self.openSessions)

    async def openSessions(self, connection):
        app = await self.iterm2.async_get_app(connection)
        window = app.current_window

        firstSession = True

        if self.inNewWindow:
            # 在新窗口中开一堆窗口
            await self.iterm2.window.Window.async_create(connection)
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
        profile = self.iterm2.LocalWriteOnlyProfile()
        # Change colour of tab
        # colour = iterm2.Color(102, 178, 255)
        # change.set_tab_color(colour)
        # change.set_use_tab_color(True)

        # Change colour of badge - text embedded into screen
        # Pull name from csv line and use for badge
        colour_badge = self.iterm2.Color(255, 255, 51, 129)
        profile.set_badge_color(colour_badge)
        profile.set_badge_text(item.get('nodeName'))

        await session.async_set_profile_properties(profile)

        # Execute the command - could be telnet, ssh etc...
        # await session.async_send_text("ssh ossuser@" + item.get('ip') + "\n")
        await session.async_send_text(ExpectParamSupport.getCmd(item))


