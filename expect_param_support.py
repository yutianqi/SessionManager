import os
import sys

class ExpectParamSupport():
    # WORK_PATH
    workPath = os.path.dirname(sys.argv[0])

    @classmethod
    def getCmd(cls, node):
        return "expect " + os.path.join(cls.workPath, "jump.exp") + " " + cls.getParams(node) + "\n"

    @classmethod
    def getParams(cls, node):
        (nodesCounter, params) = cls.getParamsFromNode(node)
        params.insert(0, str(nodesCounter))
        params.insert(1, "1")
        return " ".join(params)

    @classmethod
    def getParamsFromNode(cls, node):
        levels = 1
        params = [
            "ssh",
            node.get("username"),
            node.get("ip"),
            node.get("port"),
            "0",
            "1",
            "1",
            node.get("password")
        ]
        if node.get("commands"):
            commands = ['"' + item + '"' for item in node.get("commands")]
            params.append(str(len(commands)))
            params.extend(commands)
        else:
            params.append("0")
        params.append("0")

        if node.get("jumper"):
            (subLevels, subParams) = cls.getParamsFromNode(node.get("jumper"))
            levels += subLevels
            params.extend(subParams)
        return (levels, params)

