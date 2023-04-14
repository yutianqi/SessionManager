#!/usr/bin/env python3
# encoding=utf8

from utils.arg_utils import ArgUtils
from utils.color_utils import ColorUtils

from support.session_support import SessionSupport

class SessionAdder():

    @classmethod
    def execute(cls):
        """
        添加session功能入口
        """
        if ArgUtils.getSessionContentInTextFormat():
            print("\n {} Featurn is not implemented...\n".format(
                ColorUtils.getRedContent("✗")))
            return
        if ArgUtils.getSessionContentInJsonFormat():
            session = json.loads(ArgUtils.getSessionContentInJsonFormat())
            SessionSupport.addSessions([session])
            return
        if ArgUtils.getSessionContentInFileFormat():
            fileName = ArgUtils.getSessionContentInFileFormat()
            with open(fileName) as f:
                lines = f.readlines()
                data = json.loads("".join(lines))
                if type(data) == list:
                    SessionSupport.addSessions(data)
                elif type(data) == dict:
                    SessionSupport.addSessions([data])
                else:
                    print("\n {} Invalid format\n".format(
                        ColorUtils.getRedContent("✗")))
            return

        nodeName = input("session name: ")
        ip = input("ip: ")
        port = input("port: ")
        username = input("username: ")
        password = input("password: ")
        SessionSupport.addSession(nodeName, ip, port, username, password)
