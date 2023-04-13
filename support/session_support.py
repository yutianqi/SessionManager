

from utils.session_file_utils import SessionFileUtils



class SessionSupport():

    def getSessionNodes(sessions, ids):
        """
        从指定sessions中获取id在ids列表内的session

        :param sessions: 原始session列表
        :param sessions: 目标sessionId列表
        :returns: 目标session列表
        """
        nodes = []
        for item in sessions:
            if item.get("nodeId") in ids:
                if item.get("nodeType") == "directory":
                    # 如果是目录，则将目录下所有session添加到nodes中
                    nodes.extend(getSubSessionNodes(item))
                else:
                    # 如果是session，则该session添加到nodes中
                    nodes.append(item)
                ids.remove(item.get("nodeId"))
                if not ids:
                    return (nodes, ids)
                continue
            # 如果当前节点id不在ids中，但是包含子节点，则在自节点中继续查找
            if item.get("childNodes"):
                (subNodes, ids) = getSessionNodes(item.get("childNodes"), ids)
                if subNodes:
                    nodes.extend(subNodes)
        return (nodes, ids)


    def getSubSessionNodes(parentNode):
        """
        查询某个节点下的所有子session节点

        :param parentNode: 父节点
        :returns: 子session节点列表
        """
        nodes = []
        if not parentNode.get("childNodes"):
            # 如果没有子节点直接返回空列表
            return nodes
        for node in parentNode.get("childNodes"):
            # 如果子节点是session，则直接添加到nodes中
            if node.get("nodeType") == "session":
                nodes.append(node)
                continue
            # 如果子节点是目录，则继续查询该目录下的子节点
            nodes.extend(getSubSessionNodes(node))
        return nodes

    def getNode(sessions, id):
        """
        在sessions中查询指定id的节点

        :param id: 节点ID
        :returns: 节点对象，如果指定ID节点不存在，则返回None
        """
        for item in sessions:
            if item.get("nodeId") == id:
                return item
            if item.get("childNodes"):
                node = getNode(item.get("childNodes"), id)
                if node:
                    return node
        return None

    @classmethod
    def addSessionsInMap(cls, sessions):
        SessionFileUtils.addSessionsInMap(sessions)

    @classmethod
    def addSession(cls, nodeName, ip, port, username, password):
        SessionFileUtils.addSession(nodeName, ip, port, username, password)


    @classmethod
    def loadSessions(cls):
        return SessionFileUtils.loadSessions()
    
    @classmethod 
    def deleteSessionsMain(cls, nodeIds):
        return SessionFileUtils.deleteSessionsMain(nodeIds)
