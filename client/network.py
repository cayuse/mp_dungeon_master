from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.gui.DirectGui import *
import sys


class Player(DirectObject):
    def __init__(self):
        self.currentPos = {'x': 244, 'y': 188, 'z': 0, 'h': 0, 'p': 0, 'r': 0}  # stores rotation too
        self.isMoving = False
        self.username = ""

    def load(self):
        self.model = Actor("models/ralph",
                           {"run": "models/ralph-run",
                            "walk": "models/ralph-walk"})
        self.model.reparentTo(render)
        self.model.setScale(0.5)
        self.isMoving = False
        self.AnimControl = self.model.getAnimControl('walk')
        self.AnimControl.setPlayRate(0.05)
        self.model.setBlend(frameBlend=1)

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
            print "initializing"
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
                    print "player ", str(i), " initialized"
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
        return Task.cont



class World(DirectObject):  # This class will control anything related to the virtual world
    def __init__(self):
        self.timeSinceLastUpdate = 0

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
            try:
                clientClass.cWriter.send(self.datagram, clientClass.Connection)
            except:
                print "No connection to the server. You are in stand alone mode."
                return Task.done
            self.timeSinceLastUpdate = 0
        return Task.cont


class chatRegulator(DirectObject):
    def __init__(self, clientClass, keysClass):
        self.maxMessages = 14
        self.messageList = []
        self.client = clientClass
        self.keys = keysClass
        # for gui debug
        self.accept("p", self.getWidgetTransformsF)
        # Create GUI
        # self.frame =
        self.chatInput = DirectEntry(initialText="Press 't' or click here to chat",
                                     cursorKeys=1,
                                     numLines=1,
                                     command=self.send,
                                     focusInCommand=self.handleTpress,
                                     focusOutCommand=self.resetText,
                                     focus=0,
                                     width=20)
        # self.chatInput.setPos(-1.31667,0,-0.97)
        self.chatInput.setScale(0.05)
        self.chatInput.reparentTo(base.a2dBottomLeft)
        self.chatInput.setPos(.05, 0, .05)

        self.messages = []
        self.txt = []
        for k in range(14):
            self.txt.append(OnscreenText(mayChange=1))
            self.messages.append(DirectLabel(activeState=1, text="hi"))
            # self.messages[k].setScale(0.0498732)
            # self.messages[k].setPos(-1.31667,0,-0.9)
        self.accept("t", self.handleTpress)
        self.accept("control-t", self.resetText)
        self.calls = 0

    def handleTpress(self):
        if not self.keys.isTyping:
            self.clearText()

    def clearText(self):
        self.chatInput.enterText('')
        self.keys.isTyping = True
        self.chatInput["focus"] = True

    def resetText(self):
        self.chatInput.enterText('')
        self.keys.isTyping = False

    # def leaveText(self):
    #  self.keys.isTyping = False
    def send(self, text):
        self.datagram = PyDatagram()
        self.datagram.addString("chat")
        self.datagram.addString(text)
        self.client.cWriter.send(self.datagram, self.client.Connection)

    def setText(self, text):
        self.index = 0
        # put the messages on screen
        self.messageList.append(text)
        if (len(self.messageList) > 14):
            self.messageList.reverse()
            del self.messageList[14]
            self.messageList.reverse()
        for k in self.messageList:
            self.text(k, (-.95, (-.8 + (.06 * self.index))), self.index)
            self.index += 1

    def getWidgetTransformsF(self):
        for child in aspect2d.getChildren():
            print child, "  position = ", child.getPos()
            print child, "  scale = ", child.getScale()

    def text(self, msg, position, index):
        self.txt[index].destroy()
        self.txt[index] = OnscreenText(text=msg, pos=position, fg=(1, 1, 1, 1), align=TextNode.ALeft, scale=.05,
                                       mayChange=1)
        self.txt[index].reparentTo(base.a2dBottomLeft)
        self.txt[index].setPos(.05, .15 + .05 * index)

