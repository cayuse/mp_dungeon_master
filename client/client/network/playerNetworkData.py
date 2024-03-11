from ..myPan.myPan import base
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from ..Character import Character
import pickle
from panda3d.core import LPoint3f, LVecBase3f
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
    def processData(self, data):
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

    def processChat(self,packet):
        pass ## rework the chatclass for this nonsense
        text = packet.message
        chatClass.setText(text)

    def updatePlayers(self, m):
        if (self.numofplayers != 0):
            for k in range(int(self.numofplayers)):
                # As long as the player is not the client put it where the server says
                if (k != m.playernum):
                    self.playerList[k].model.setPosHpr(self.playerList[k].currentPos['x'],
                                                       self.playerList[k].currentPos['y'],
                                                       self.playerList[k].currentPos['z'],
                                                       self.playerList[k].currentPos['h'],
                                                       self.playerList[k].currentPos['p'],
                                                       self.playerList[k].currentPos['r'])
                    #ism = self.playerList[k].isMoving
                    #print(ism)
                    if (self.playerList[k].isMoving):
                        self.playerList[k].model.loop("walk")
                    else:
                        self.playerList[k].model.pose("walk", 5)
        return Task.cont
    def UpdateWorld(self, meClass, clientClass):
        # get the time since the last framerate
        self.elapsed = globalClock.getDt()
        # add it to the time since we last set our position to where the server thinks we are
        # add the elapsed time to the time since the last update sent to the server
        self.timeSinceLastUpdate += self.elapsed
        if (self.timeSinceLastUpdate > 0.1):
            self.datagram = PyDatagram()
            self.datagram.addString("positions")
            self.datagram.addFloat64(meClass.model.getX())
            self.datagram.addFloat64(meClass.model.getY())
            self.datagram.addFloat64(meClass.model.getZ())
            self.datagram.addFloat64(meClass.model.getH())
            self.datagram.addFloat64(meClass.model.getP())
            self.datagram.addFloat64(meClass.model.getR())
            self.datagram.addBool(meClass.isMoving)
            try:
                clientClass.cWriter.send(self.datagram, clientClass.Connection)
            except:
                print("No connection to the server. You are in stand alone mode.")
                return Task.done
            self.timeSinceLastUpdate = 0
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

    def UpdateWorld(self, meClass, clientClass):
        # get the time since the last framerate
        self.elapsed = globalClock.getDt()
        # add it to the time since we last set our position to where the server thinks we are
        # add the elapsed time to the time since the last update sent to the server
        self.timeSinceLastUpdate += self.elapsed
        if (self.timeSinceLastUpdate > 0.1):
            self.datagram = PyDatagram()
            self.datagram.addString("positions")
            self.datagram.addFloat64(meClass.model.getX())
            self.datagram.addFloat64(meClass.model.getY())
            self.datagram.addFloat64(meClass.model.getZ())
            self.datagram.addFloat64(meClass.model.getH())
            self.datagram.addFloat64(meClass.model.getP())
            self.datagram.addFloat64(meClass.model.getR())
            self.datagram.addBool(meClass.isMoving)
            try:
                clientClass.cWriter.send(self.datagram, clientClass.Connection)
            except:
                print("No connection to the server. You are in stand alone mode.")
                return Task.done
            self.timeSinceLastUpdate = 0
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