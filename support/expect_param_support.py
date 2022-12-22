#!/usr/bin/env python3
# encoding=utf8

import os
import sys
import json

class ExpectParamSupport():
    workPath = os.path.dirname(sys.argv[0])

    @classmethod
    def getCmd(cls, node):
        return "expect {} {}\n".format(os.path.join(cls.workPath, "support", "jump.exp"), cls.getParams(node))

    @classmethod
    def getParams(cls, node):
        (nodesCounter, params) = cls.getParamsFromNode(node)
        return " ".join(params)

    @classmethod
    def getParamsFromNode(cls, node):
        levels = 1
        params = [
            "ssh",
            node.get("username"),
            node.get("ip"),
            node.get("port"),
            '"' + node.get("password") + '"'
        ]
        if node.get("commands"):
            commands = []
            for item in node.get("commands"):
                expect = item.get("expect")
                send = item.get("send")
                commands.append('"' + expect + '"')
                commands.append('"' + send + '"')
            params.append(str(len(commands)))
            params.extend(commands)
        else:
            params.append("0")

        if node.get("jumper"):
            (subLevels, subParams) = cls.getParamsFromNode(node.get("jumper"))
            levels += subLevels
            params.extend(subParams)
        return (levels, params)



if __name__ == "__main__":
    rawJson = """{
                    "nodeName": "Disb1_1",
                    "nodeType": "session",
                    "ip": "10.50.135.106",
                    "port": "22",
                    "username": "ossuser",
                    "password": "Huawei@Cloud8#",
                    "jumper": {
                        "ip": "10.50.135.106",
                        "port": "22",
                        "username": "ossadm",
                        "password": "Huawei@Cloud8#",
                        "commands": [
                            {"expect": "$ ","send": "su -"},
                            {"expect": "Password","send": "Huawei@Cloud8#"},
                            {"expect": "# ","send": "su - dbuser"}
                        ]
                    },
                    "nodeId": 31
                }"""
    node = json.loads(rawJson)
    # expect t.exp ssh ossuser 10.50.135.106 22 "Huawei@Cloud8#" 0 ssh ossadm 10.50.135.106 22 "Huawei@Cloud8#" 6 "$ " "su -" "Password" "Huawei@Cloud8#" "# " "su - dbuser"
    print(ExpectParamSupport.getCmd(node))

