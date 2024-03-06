#from panda3d.core import *
#from direct.showbase.ShowBase import ShowBase
from .myPan.myPan import base
from direct.showbase.DirectObject import DirectObject
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.actor.Actor import Actor
from direct.task.Task import Task
from panda3d.core import TextNode
from direct.gui.DirectGui import *
from direct.interval import ProjectileInterval
#base = ShowBase()
base.enableParticles()
from direct.particles.ParticleEffect import ParticleEffect
import sys

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

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
        self.chatInput = DirectEntry(initialText="Press 't' to chat",
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
            print(child, "  position = ", child.getPos())
            print(child, "  scale = ", child.getScale())

    def text(self, msg, position, index):
        self.txt[index].destroy()
        self.txt[index] = OnscreenText(text=msg, pos=position, fg=(1, 1, 1, 1), align=TextNode.ALeft, scale=.05,
                                       mayChange=1)
        self.txt[index].reparentTo(base.a2dBottomLeft)
        self.txt[index].setPos(.05, .15 + .05 * index)

