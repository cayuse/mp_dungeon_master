from ..myPan.myPan import base, modelPath, playerScale
from direct.showbase.DirectObject import DirectObject
from panda3d.core import AnimControl
from panda3d.core import NodePath, PandaNode
from direct.actor.Actor import Actor


class playerCharacter(DirectObject):
    def __init__(self):
        super().__init__()
        self.model = None

    def getModel(self):
        return self.model
