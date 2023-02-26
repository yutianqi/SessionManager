#!/usr/bin/python
# encoding='utf-8'

import sys
import pexpect
import struct
import fcntl
import termios
import signal

# python jump.py ssh pi 192.168.28.31 22 pi@98842674 0 ssh duke 192.168.28.31 22 duke@98842674 0


def sigwinch_passthrough(sig, data):
    winsize = getwinsize()
    global child
    child.setwinsize(winsize[0], winsize[1])


def getwinsize():
    """This returns the window size of the child tty.
    The return value is a tuple of (rows, cols).
    """
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1024  # Assume
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]


def login(user, passwd, host):
    print('ssh ' + user + '@' + host + ' ...')

    logFileId = open("logfile.txt", 'wb')
    # child = pexpect.spawn('ssh ' + user + '@' + host , env = {"TERM" : "xterm-256color"}, logfile=logFileId)
    child = pexpect.spawn('ssh ' + user + '@' + host,
                          env={"TERM": "xterm-256color"}, logfile=logFileId, encoding='utf-8')

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

    winsize = getwinsize()

    while(argvs):
        protocol = argvs.pop(0)
        username = argvs.pop(0)
        host = argvs.pop(0)
        port = argvs.pop(0)
        password = argvs.pop(0)

        cmd = "{} -p {} {}@{}".format(protocol, port, username, host)
        if not child:
            print(cmd)
            # child = pexpect.spawn(cmd, env = {"TERM" : "xterm-256color"}, logfile=open("logfile.txt", 'w'))
            # child = pexpect.spawn(cmd, env = {"TERM" : "xterm-256color"}, logfile=open("logfile.txt", 'w'), encoding='utf-8')
            child = pexpect.spawn(
                cmd, env={"TERM": "xterm-256color"}, logfile=sys.stdout, encoding='utf-8')
        else:
            child.expect('###')
            print(cmd)
            child.sendline(cmd)

        '''
        pi@raspberrypi:~ $### ssh duke@192.168.28.31
        The authenticity of host '192.168.28.31 (192.168.28.31)' can't be established.
        ECDSA key fingerprint is SHA256:H2ETqWQ4/KSC8qJbt0G2O5ENEuNWN8hzl9+y0Rjs9nM.
        Are you sure you want to continue connecting (yes/no)? yes
        Warning: Permanently added '192.168.28.31' (ECDSA) to the list of known hosts.
        duke@192.168.28.31's password:
        '''
        child.expect('.*password:.*')
        child.sendline(password)

        cmdNum = int(argvs.pop(0))
        for i in range(cmdNum):
            print(i)
            expectContent = argvs.pop(0).replace("\\\\", "\\")
            print("expcet: " + expectContent)
            child.expect(expectContent)
            sendContent = argvs.pop(0)
            print("send: " + sendContent)
            child.sendline(sendContent)

    signal.signal(signal.SIGWINCH, sigwinch_passthrough)
    child.setwinsize(winsize[0], winsize[1])

    child.logfile = None
    child.interact()
    pass

    # user   = 'ossuser'
    # passwd = 'Huawei@Cloud8#'
    # host   = '120.46.207.204'
    # login(user, passwd, host)
