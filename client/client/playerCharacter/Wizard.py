from ..myPan.myPan import base, modelPath, playerScale
from direct.showbase.DirectObject import DirectObject
from panda3d.core import AnimControl
from panda3d.core import NodePath, PandaNode
from direct.actor.Actor import Actor
from .playerCharacter import playerCharacter

class Wizard(playerCharacter):
    def __init__(self):
        super().__init__()

        self.model = Actor(modelPath + "male2",
                           {"walk": modelPath + "male2_walk",
                            "strafe": modelPath + "male2_strafe",
                            "idle": modelPath + "male2_idle",
                            "attack1": modelPath + "male2_attack1",
                            "attack2": modelPath + "male2_raize",
                            "hit": modelPath + "male2_hit",
                            "block": modelPath + "male2_raize2",
                            "die": modelPath + "male2_die"
                            })

        self.model.setScale((playerScale, playerScale, playerScale))
        #self.AnimControl.setPlayRate(0.05)
        self.model.setBlend(frameBlend=1)

