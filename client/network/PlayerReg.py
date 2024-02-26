from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from . import Player

class PlayerReg(DirectObject):  # This class will regulate the players
    def __init__(self):
        self.playerList = []
        self.numofplayers = 0
        self.enemy1 = []
        self.numofenemy1 = 0
    def ProcessData(self, datagram, m, chatClass):
        # process received data
        self.iterator = PyDatagramIterator(datagram)
        self.type = self.iterator.getString()
        if (self.type == "init"):
            print("initializing")
            # initialize
            m.setPlayerNum(self.iterator.getUint8())
            self.num = self.iterator.getFloat64()
            for i in range(int(self.num)):
                if (i != m.playernum):
                    self.playerList.append(Player())
                    self.playerList[i].username = self.iterator.getString()
                    self.playerList[i].load()
                    self.playerList[i].currentPos['x'] = self.iterator.getFloat64()
                    self.playerList[i].currentPos['y'] = self.iterator.getFloat64()
                    self.playerList[i].currentPos['z'] = self.iterator.getFloat64()
                    print("player ", str(i), " initialized")
                else:
                    self.playerList.append(Player())
            self.numofplayers = self.num
        if (self.type == "update"):
            self.num = self.iterator.getFloat64()
            if (self.num > self.numofplayers):
                for i in range(int(self.numofplayers)):
                    self.playerList[i].currentPos['x'] = self.iterator.getFloat64()
                    self.playerList[i].currentPos['y'] = self.iterator.getFloat64()
                    self.playerList[i].currentPos['z'] = self.iterator.getFloat64()
                    self.playerList[i].currentPos['h'] = self.iterator.getFloat64()
                    self.playerList[i].currentPos['p'] = self.iterator.getFloat64()
                    self.playerList[i].currentPos['r'] = self.iterator.getFloat64()
                    self.playerList[i].isMoving = self.iterator.getBool()
                for i in range(int(self.numofplayers), int(self.num)):
                    if (i != m.playernum):
                        self.playerList.append(Player())
                        self.playerList[i].load()
                        self.playerList[i].currentPos['x'] = self.iterator.getFloat64()
                        self.playerList[i].currentPos['y'] = self.iterator.getFloat64()
                        self.playerList[i].currentPos['z'] = self.iterator.getFloat64()
                        self.playerList[i].currentPos['h'] = self.iterator.getFloat64()
                        self.playerList[i].currentPos['p'] = self.iterator.getFloat64()
                        self.playerList[i].currentPos['r'] = self.iterator.getFloat64()
                        self.playerList[i].isMoving = self.iterator.getBool()
                    else:
                        self.playerList.append(Player())
                self.numofplayers = self.num
            else:
                for i in range(int(self.numofplayers)):
                    self.playerList[i].currentPos['x'] = self.iterator.getFloat64()
                    self.playerList[i].currentPos['y'] = self.iterator.getFloat64()
                    self.playerList[i].currentPos['z'] = self.iterator.getFloat64()
                    self.playerList[i].currentPos['h'] = self.iterator.getFloat64()
                    self.playerList[i].currentPos['p'] = self.iterator.getFloat64()
                    self.playerList[i].currentPos['r'] = self.iterator.getFloat64()
                    self.playerList[i].isMoving = self.iterator.getBool()
        if (self.type == "chat"):
            self.text = self.iterator.getString()
            chatClass.setText(self.text)

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
