#from panda3d.core import *
from .myPan.myPan import base
from direct.showbase.DirectObject import DirectObject
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.gui.DirectGui import *
from direct.interval import ProjectileInterval
base.enableParticles()
from direct.particles.ParticleEffect import ParticleEffect
import sys

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class Keys(DirectObject):
    def __init__(self):
        self.isTyping = False
        self.keyMap = {"left": 0, "right": 0, "forward": 0, "back": 0, "cam": 0, "right": 0, "autoRun": 0, "fire1": 0}
        #Quits game
        self.accept("escape", sys.exit)

        self.accept(",", self.setKey, ["forward", 1])
        self.accept(",-up", self.setKey, ["forward", 0])
        self.accept("w", self.setKey, ["forward", 1])
        self.accept("w-up", self.setKey, ["forward", 0])

        self.accept("a", self.setKey, ["left", 1])
        self.accept("a-up", self.setKey, ["left", 0])

        self.accept("o", self.setKey, ["back", 1])
        self.accept("o-up", self.setKey, ["back", 0])
        self.accept("d", self.setKey, ["back", 1])
        self.accept("d-up", self.setKey, ["back", 0])

        self.accept("e", self.setKey, ["right", 1])
        self.accept("e-up", self.setKey, ["right", 0])
        self.accept("s", self.setKey, ["right", 1])
        self.accept("s-up", self.setKey, ["right", 0])

        self.accept("mouse1",  self.setKey, ["fire1", 1])
        self.accept("mouse1-up", self.setKey,["fire1", 0])
        self.accept("wheel_up", self.setKey, ["wheel-in", 1])
        self.accept("wheel_down", self.setKey, ["wheel-out", 1])
        self.accept("page_up", self.setKey, ["zoom-in", 1])
        self.accept("page_up-up", self.setKey, ["zoom-in", 0])
        self.accept("page_down", self.setKey, ["zoom-out", 1])
        self.accept("page_down-up", self.setKey, ["zoom-out", 0])

    def setKey(self, key, value):
        if not self.isTyping:
            self.keyMap[key] = value

    def autoRun(self):
        if not self.keyMap["autoRun"]:
            self.setKey("autoRun", 1)
            self.setKey("forward", 1)
        else:
            self.setKey("autoRun", 0)
            self.setKey("forward", 0)
