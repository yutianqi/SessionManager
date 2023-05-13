#!/usr/bin/env python3
# encoding=utf8

from utils.session_file_utils import SessionFileUtils

class SessionSupport():
    """
    Session管理
    """

    @classmethod
    def addSession(cls, nodeName, ip, port, username, password):
        """
        在sessions中查询指定id的节点

        :param id: 节点ID
        :returns: 节点对象，如果指定ID节点不存在，则返回None
        """
        session = {
            "nodeName": nodeName,
            "nodeType": "session",
            "ip": ip,
            "port": port,
            "username": username,
            "password": password
        }
        cls.addSessions([session])

    @classmethod
    def addSessions(cls, sessions):
        """
        添加Session

        :param sessions: Session列表
        """
        SessionFileUtils.addSessions(sessions)

    @classmethod 
    def deleteSessions(cls, nodeIds):
        """
        删除Session

        :param nodeIds: 待删除节点列表
        """
        return SessionFileUtils.deleteSessions(nodeIds)

    @classmethod
    def getNodes(cls, sessions=[], nodeIds=[]):
        """
        从指定Sessions中查询指定ID的Session列表

        :param sessions: Session列表
        :param sessions: 目标节点Id列表
        :returns: 目标Session列表
        """
        # 如果未指定Session列表，则默认从全量Session中查找
        if not sessions:
            (total, sessions) = SessionFileUtils.loadSessions()
        # 如果未指定目标节点ID列表，则默认返回全量Session列表
        if not nodeIds:
            return (sessions, [])
        nodes = []
        for item in sessions:
            if item.get("nodeId") in nodeIds:
                if item.get("nodeType") == "directory":
                    # 如果是目录，则将目录下所有session添加到nodes中
                    nodes.extend(cls.getSubSessionNodes(item))
                else:
                    # 如果是session，则该session添加到nodes中
                    nodes.append(item)
                nodeIds.remove(item.get("nodeId"))
                if not nodeIds:
                    return (nodes, nodeIds)
                continue
            # 如果当前节点id不在nodeIds中，但是包含子节点，则在自节点中继续查找
            if item.get("childNodes"):
                (subNodes, nodeIds) = cls.getNodes(item.get("childNodes"), nodeIds)
                if subNodes:
                    nodes.extend(subNodes)
        return (nodes, nodeIds)

    @classmethod
    def getNode(cls, nodeId="", sessions=[]):
        """
        从Sessions查询指定ID的节点对象

        :param sessions: Session列表
        :param sessions: 目标节点Id
        :returns: 目标节点对象(可能是目录，也可能是session)
        """
        # 如果未指定Session列表，则默认从全量Session中查找
        if not sessions:
            (total, sessions) = SessionFileUtils.loadSessions()
        # print(sessions)
        # 如果未指定目标节点ID，则默认返回根Session
        if not nodeId:
            return sessions
        nodes = []
        for item in sessions:
            if item.get("nodeId") == nodeId:
                return item
            if item.get("nodeType") == "session":
                continue
            # 继续从子节点中查找
            ret = cls.getNode(item.get("childNodes"), nodeId)
            if ret:
                return ret
        return None

    @classmethod
    def getSubSessionNodes(cls, parentNode):
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
            nodes.extend(cls.getSubSessionNodes(node))
        return nodes




    