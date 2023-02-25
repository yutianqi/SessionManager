#!/usr/bin/python

import sys
import time
import pexpect
import struct
import fcntl
import termios
import signal

def sigwinch_passthrough (sig, data):
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
    user   = 'ossuser'
    passwd = 'Huawei@Cloud8#'
    host   = '120.46.207.204'

    login(user, passwd, host)