from ..myPan.myPan import base
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from ..Character import Character
import pickle
from panda3d.core import LPoint3f, LVecBase3f
from dataclasses import dataclass


@dataclass
class playerPacket:
    type = "None"
    message = "None"
    playerNum = 0
    Pos = LPoint3f(0, 0, 0)
    Hpr = LVecBase3f(0, 0, 0)
    playerName = None
    characterType = None


class PlayerReg(DirectObject):  # This class will regulate the players
    def __init__(self):
        self.playerList = {}
        self.numofplayers = 0
        self.enemy1 = []
        self.numofenemy1 = 0

    def tskProcessData(self, data):
        # process received data
        packet = pickle.loads(data)
        type = packet.type
        if type == "None":
            return Task.cont
        if (type == "init"):
            self.processInit(packet)
        if (type == "update"):
            self.processUpdate(packet)
        if (type == "chat"):
            self.processChat(packet)
        return Task.cont

    def processInit(self, packet):
        print("initializing")
        plr = packet.playerNum
        if plr in self.playerList:
            thisPlayer = self.playerList[plr]
        else:
            thisPlayer = Character()
            self.playerList[plr] = thisPlayer
        thisPlayer.setCharacter(packet.characterType)
        thisPlayer.setPlayerNum(packet.playerNum)
        thisPlayer.getRoot().reparantTo(base.render)

    def processUpdate(self, packet):
        plr = packet.playerNum
        thisPlayer = self.playerList[plr]
        thisPlayer.setPos(packet.Pos)
        thisPlayer.setHpr(packet.Hpr)

    def processChat(self, packet):
        pass  ## rework the chatclass for this nonsense
        text = packet.message
        # chatClass.setText(text)

    def tskUpdateWorld(self, me):
        packet = playerPacket()
        playerPacket.Pos = me.getPos()
        playerPacket.Hpr = me.getHpr()
        serialized_data = pickle.dumps(playerPacket)
        try:
            clientClass.cWriter.send(serialized_data)
        except:
            print("No connection to the server. You are in stand alone mode.")
            return Task.done
        return Task.cont

    def UpdateName(self, meClass, clientClass):
        print("update name entered")
        self.datagram = PyDatagram()
        self.datagram.addString("newname")
        self.datagram.addString(meClass.username)
        try:
            clientClass.cWriter.send(self.datagram, clientClass.Connection)
        except:
            print("No connection to the server. You are in stand alone mode.")

    def UpdateName(self, meClass, clientClass):
        print("update name entered")
        self.datagram = PyDatagram()
        self.datagram.addString("newname")
        self.datagram.addString(meClass.username)
        try:
            clientClass.cWriter.send(self.datagram, clientClass.Connection)
        except:
            print("No connection to the server. You are in stand alone mode.")
