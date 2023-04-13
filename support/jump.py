#!/usr/bin/python
# encoding='utf-8'

import sys
import pexpect
import struct
import fcntl
import termios
import signal

# Usage:
#   python jump.py ssh pi 192.168.28.31 22 pi@98842674 0 ssh duke 192.168.28.31 22 duke@98842674 0
#   python jump.py ssh pi 192.168.28.31 22 pi@98842674 1 "###" "touch abc.txt" ssh duke 192.168.28.31 22 duke@98842674 0
#   python jump.py ssh ubuntu 54.82.85.66 22 _2021@NetEco98842674 1 "\s" "touch abc.txt"


child = None


def sigwinch_passthrough(sig, data):
    """
    窗口表更事件回调方法
    """
    winsize = getwinsize()
    global child
    child.setwinsize(winsize[0], winsize[1])


def getwinsize():
    """
    This returns the window size of the child tty.
    The return value is a tuple of (rows, cols).
    """
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1024  # Assume
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]


def execute(argvs):
    """
    执行入口
    """
    global child
    while(argvs):
        protocol = argvs.pop(0)
        username = argvs.pop(0)
        host = argvs.pop(0)
        port = argvs.pop(0)
        password = argvs.pop(0)

        cmd = """{} -p {} {}@{}""".format(protocol, port, username, host)
        # print(cmd)
        if not child:
            # child = pexpect.spawn(cmd, env = {"TERM" : "xterm-256color"}, logfile=open("logfile.txt", 'w'), encoding='utf-8')
            child = pexpect.spawn(
                cmd, env={"TERM": "xterm-256color"}, logfile=sys.stdout, encoding='utf-8')
        else:
            child.expect('\$.*')
            child.sendline(cmd)

        # 如果之前已登录过，会提示输入password，如果之前没登录过，需要确认信任


        try:
            ret = child.expect(['.*password:.*', '.*yes/no.*'])
        except pexpect.exceptions.TIMEOUT:
            print("timeout")
            return

        if ret == 0:
            child.sendline(password)
        else:
            child.sendline("yes")
            ret = child.expect(['.*password:.*', '.*yes/no.*'])
            child.sendline(password)

        # 执行子命令
        subCmdNum = int(argvs.pop(0))
        for i in range(subCmdNum):
            # print(i)
            expectContent = argvs.pop(0).replace("\\\\", "\\")
            # print("expcet: " + expectContent)
            child.expect(expectContent)
            sendContent = argvs.pop(0)
            # print("send: " + sendContent)
            child.sendline(sendContent)


    winsize = getwinsize()
    child.setwinsize(winsize[0], winsize[1])
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)

    child.logfile = None
    child.interact()
    pass


if __name__ == '__main__':
    argvs = sys.argv
    # print(argvs)
    fileName = argvs.pop(0)
    execute(argvs)
