#!/usr/bin/env python3
# encoding=utf8

from asyncore import close_all
import json
import os
import sys
import time

class SessionFileUtils():
    WORK_PATH = os.path.dirname(sys.argv[0])
    rowJson = {}
    maxNodeId = 0
    
    @classmethod
    def getRowJson(cls):
        if cls.rowJson:
            return cls.rowJson
        with open(os.path.join(cls.WORK_PATH, "sessions.json")) as f:
            lines = f.readlines()
            cls.rowJson = json.loads("".join(lines))
        return cls.rowJson
    
    @classmethod
    def loadSessions(cls):
        sessions = cls.getRowJson()
        return (sessions.get("total"), sessions.get("nodes"))

    @classmethod
    def addSession(cls, nodeName, ip, port, username, password):
        session = {
            "nodeName": nodeName,
            "nodeType": "session",
            "ip": ip,
            "port": port,
            "username": username,
            "password": password
        }
        cls.addSessionsInMap([session])
        
    @classmethod
    def addSessionsInMap(cls, sessions):
        for session in sessions:
            cls.arrangeNodeId(session)
        rowJson = cls.getRowJson()
        rowJson.get("nodes").extend(sessions)
        rowJson["updateTime"] = int(time.time())
        rowJson["total"] = cls.getTotal(rowJson.get("nodes"))
        cls.saveSessionsToFile()

    @classmethod
    def deleteSessionsMain(cls, ids):
        rowJson = cls.getRowJson()
        deletedNodeIds = cls.deleteSessions(rowJson.get("nodes"), ids)
        rowJson["updateTime"] = int(time.time())
        rowJson["total"] = cls.getTotal(rowJson.get("nodes"))
        cls.saveSessionsToFile()
        return deletedNodeIds

    @classmethod
    def deleteSessions(cls, nodes, ids):
        deletedNodeIds = []
        for item in nodes[::-1]:
            if item.get("nodeId") in ids:
                nodes.remove(item)
                deletedNodeIds.append(item.get("nodeId"))
                continue
            if item.get("childNodes"):
                childDeletedNodeIds = cls.deleteSessions(item.get("childNodes"), ids)
                if childDeletedNodeIds:
                    deletedNodeIds.extend(childDeletedNodeIds)
        return deletedNodeIds

    @classmethod
    def getTotal(cls, nodes):
        total = 0
        for item in nodes:
            if item.get("nodeType") == 'session':
                total += 1
                continue
            if item.get("childNodes"):
                total += cls.getTotal(item.get("childNodes"))
        return total

    @classmethod
    def getNewNodeId(cls):
        if not cls.maxNodeId:
            sessions = cls.getRowJson()
            cls.maxNodeId = cls.getMaxNodeId(sessions.get("nodes"))
        cls.maxNodeId += 1
        return cls.maxNodeId

    @classmethod
    def getMaxNodeId(cls, nodes):
        maxNodeId = 0
        for item in nodes:
            if item.get("nodeId") > maxNodeId:
                maxNodeId = item.get("nodeId")
            if item.get("childNodes"):
                maxNodeIdInChildNodes = cls.getMaxNodeId(item.get("childNodes"))
                if maxNodeIdInChildNodes > maxNodeId:
                    maxNodeId = maxNodeIdInChildNodes
        return maxNodeId

    @classmethod
    def saveSessionsToFile(cls):
        with open(os.path.join(cls.WORK_PATH, "sessions.json"), "w", encoding="utf-8") as f:
            json.dump(cls.getRowJson(), f)
    
    @classmethod
    def arrangeNodeId(cls, node):
        node["nodeId"] = cls.getNewNodeId()
        if node.get("childNodes"):
            for item in node.get("childNodes"):
                cls.arrangeNodeId(item)
