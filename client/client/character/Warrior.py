from ..myPan.myPan import base, modelPath, playerScale
from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath, PandaNode
from .Character import Character
from direct.actor.Actor import Actor

class Warrior(Character):
    def __init__(self):
        super().__init__()

        self.model = Actor(modelPath + "male2",
                           {"walk": modelPath + "male_walk",
                            "strafe": modelPath + "male_strafe",
                            "idle": modelPath + "male_idle",
                            "attack1": modelPath + "male_attack1",
                            "attack2": modelPath + "male_attack2",
                            "hit": modelPath + "male_hit",
                            "block": modelPath + "male_block",
                            "die": modelPath + "male_die"
                            })

        self.model.setScale((playerScale, playerScale, playerScale))
        self.model.reparentTo(self.charNode)

