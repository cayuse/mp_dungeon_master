from .myPan.myPan import base, modelPath, modelIdleTime
from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath, PandaNode
from .playerCharacter import Archer, Sorceress, Warrior, Wizard

pcs = {"Wizard": Wizard, "Archer": Archer, "Warrior": Warrior, "Sorceress": Sorceress}

class Character(DirectObject):
    def __init__(self, type="wizard"):
        self.charNode = NodePath(PandaNode("CharacterNode"))
        self.charNode.reparentTo(base.render)
        self.charNode.setPos(0, 0, 0)
        self.charNode.setHpr(0, 0, 0)

        self.model = None  # child class needs to define a model
        self.modelClass = None
        self.playerNum = None

    def setPlayerNum(self, num):
        self.playerNum = num
    def getPlayerNum(self):
        return self.playerNum
    def walk(self):
        self.model.stop()
        self.model.loop("walk")

    def stop(self):
        self.model.stop()
        self.model.pose("walk", 5)

    def idle(self):
        self.model.stop()
        self.model.loop("idle")

    def strafe(self):
        self.model.stop()
        self.model.loop("strafe")

    def getRoot(self):
        return self.charNode

    def setCharacter(self, character="Wizard"):
        if self.model is not None:
            self.modelClass.destroy()
            self.model = None

        self.modelClass = pcs[character]()
        self.model = self.modelClass.getModel()
        self.model.reparentTo(self.charNode)

    def setPos(self, Pos):
        self.charNode.setPos(Pos)
    def setHpr(self, Hpr):
        self.charNode.setHpr(Hpr)
