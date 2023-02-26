#!/usr/bin/python

import sys
import pexpect

# python jump.py ssh pi 192.168.28.31 22 pi@98842674 0 ssh duke 192.168.28.31 22 duke@98842674 0

def login(username, passwd, host, expectContent, sendContent):

    cmd = "{} -p {} {}@{}".format("ssh", "22", username, host)
    print(cmd)
    child = pexpect.spawn(cmd, env = {"TERM" : "xterm-256color"}, logfile=sys.stdout, encoding='utf-8')
    
    child.expect('.*password:.*')
    child.sendline(passwd)

    child.expect(expectContent)
    child.sendline(sendContent)

    child.logfile = None
    child.interact()
    pass



if __name__ == '__main__':
    # username = "duke", 
    # passwd = "duke@98842674"
    # host = "192.168.28.31"

    username = "ubuntu" 
    passwd = "_2021@NetEco98842674"
    host = "54.82.85.66"
    expectContent = "\$ "
    sendContent = "touch abc.txt"
    # login(username, passwd, host, expectContent, sendContent)


    print(expectContent)
    print(sys.argv[1])