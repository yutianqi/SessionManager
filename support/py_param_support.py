#!/usr/bin/env python3
# encoding=utf8

import os
import sys
import json

class PyParamSupport():

    workPath = os.path.dirname(sys.argv[0])


    @classmethod
    def getCmd(cls, node):
        """
        根据节点信息生成expect命令

        :param node: 节点对象
        :returns: expect命令字符串
        """
        return "python3 {} {}\n".format(os.path.join(cls.workPath, "support", "jump.py"), " ".join(cls.getParamsFromNode(node)))


    @classmethod
    def getParamsFromNode(cls, node):
        """
        生成某个节点的expect命令入参列表

        :param node: 节点对象
        :returns: 某个节点的expect命令入参列表
        """
        params = []
        if node.get("jumper"):
            subParams = cls.getParamsFromNode(node.get("jumper"))
            params.extend(subParams)
        params.extend([
            "ssh",
            node.get("username"),
            node.get("ip"),
            node.get("port"),
            '"' + node.get("password") + '"'
        ])
        if node.get("expectCmds"):
            commands = []
            for item in node.get("expectCmds"):
                expect = item.get("expect")
                send = item.get("send")
                commands.append('"' + expect + '"')
                commands.append('"' + send + '"')
            params.append(str(len(commands)))
            params.extend(commands)
        else:
            params.append("0")
        return params


if __name__ == "__main__":
    rawJson = """{
                    "nodeName": "Disb1_1",
                    "nodeType": "session",
                    "ip": "127.0.0.1",
                    "port": "22",
                    "username": "ossuser",
                    "password": "Huawei@Cloud8#",
                    "jumper": {
                        "ip": "10.50.135.106",
                        "port": "22",
                        "username": "ossadm",
                        "password": "Huawei@Cloud8#"
                    },
                    "nodeId": 31,
                    "expectCmds": [
                        {"expect": "$ ","send": "su -"},
                        {"expect": "Password","send": "Huawei@Cloud8#"},
                        {"expect": "# ","send": "su - dbuser"}
                    ]
                }"""
    node = json.loads(rawJson)
    # expect t.exp ssh ossuser 10.50.135.106 22 "Huawei@Cloud8#" 0 ssh ossadm 10.50.135.106 22 "Huawei@Cloud8#" 6 "$ " "su -" "Password" "Huawei@Cloud8#" "# " "su - dbuser"
    print(PyParamSupport.getCmd(node))

