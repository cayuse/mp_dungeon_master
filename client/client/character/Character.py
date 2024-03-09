from ..myPan.myPan import base, modelPath, modelIdleTime
from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath, PandaNode
from direct.actor.Actor import Actor


class Character(DirectObject):
    def __init__(self):
        self.charNode = NodePath(PandaNode("CharacterNode"))
        self.charNode.reparentTo(base.render)
        self.charNode.setPos(0, 0, 0)
        self.charNode.setHpr(0,0,0)

        self.playernum = None

    def walk(self):
        self.model.stop()
        self.model.loop("walk")

    def stop(self):
        self.model.stop()
        self.model.pose("walk", 5)
        self.isMoving = False

    def idle(self):
        self.model.stop()
        self.model.loop("idle")

    def strafe(self):
        self.model.stop()
        self.model.loop("strafe")

    def getRoot(self):
        return self.charNode