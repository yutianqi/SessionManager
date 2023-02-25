#!/usr/bin/python

import sys
import time
import pexpect
import struct
import fcntl
import termios
import signal

# jump.py ssh ubuntu 34.229.204.20 22 _2021@NetEco 0 ssh ubuntu 34.229.204.20 22 _2021@NetEco 1 "$ " "touch abc.txt"

def sigwinch_passthrough(sig, data):
    winsize = getwinsize()
    global child
    child.setwinsize(winsize[0],winsize[1])

def getwinsize():
    """This returns the window size of the child tty.
    The return value is a tuple of (rows, cols).
    """
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1024 # Assume
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]


def login(user, passwd, host):
    print('ssh ' + user + '@' + host + ' ...')
    
    logFileId= open("logfile.txt", 'wb')

    child = pexpect.spawn('ssh ' + user + '@' + host , env = {"TERM" : "xterm-256color"}, logfile=logFileId)
    
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)
    
    winsize = getwinsize()
    child.setwinsize(winsize[0], winsize[1])
    
    child.expect('.*password:.*')
    child.sendline(passwd)

    # child.interact()
    
    child.expect('~]\$')
    cmd = "ssh ossadm@127.0.0.1"
    print(cmd)
    child.sendline(cmd)

    child.expect('.*password:.*')
    child.sendline(passwd)

    child.interact()
    pass


if __name__ == '__main__':
    argvs = sys.argv
    print(argvs)
    fileName = argvs.pop(0)
    print(fileName)

    child = None
    logFileId= open("logfile.txt", 'wb')

    winsize = getwinsize()

    while(argvs):
        protocol = argvs.pop(0)
        username = argvs.pop(0)
        host = argvs.pop(0)
        port = argvs.pop(0)
        password = argvs.pop(0)

        if not child:
            cmd = "{} -p {} {}@{}".format(protocol, port, username, host)
            print(cmd)
            child = pexpect.spawn(cmd, env = {"TERM" : "xterm-256color"}, logfile=logFileId)
        child.expect('.*password:.*')
        child.sendline(password)

        cmdNum = int(argvs.pop(0))
        for i in range(cmdNum):
            expectContent = argvs.pop(0).replace("\\\\", "\\")
            print("expcet: " + expectContent)
            child.expect(expectContent)
            print("send: " + sendContent)
            sendContent = argvs.pop(0)
            child.sendline(sendContent)

    signal.signal(signal.SIGWINCH, sigwinch_passthrough)
    child.setwinsize(winsize[0],winsize[1])
    child.interact()
    pass



    # user   = 'ossuser'
    # passwd = 'Huawei@Cloud8#'
    # host   = '120.46.207.204'
    # login(user, passwd, host)


