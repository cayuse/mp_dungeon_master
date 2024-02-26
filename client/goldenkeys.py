from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
import sys
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class GoldenKeys(DirectObject):  # This class will regulate the players
    def __init__(self):
        with open ("models/keys.yaml") as stream:
            keys = load(stream, Loader=Loader)
        #stream = file('models/keys.yaml', 'r')
        #keys = load(stream)
        fire = loader.loadTexture("models/fire-key.png")
        ice  = loader.loadTexture("models/ice-key.png")
        gold = loader.loadTexture("models/golden-key.tif")
        for key in keys:
            self.key = loader.loadModel("models/golden-key")
            if key[2] == 'f':
                self.key.setTexture(fire,1)
            elif key[2] == 'i':
                self.key.setTexture(ice,1)
            else:
                self.key.setTexture(gold,1)
            self.key.reparentTo(render)
            self.key.setPosHprScale(key[0],key[1],1,0,90,0,1,1,1)
            self.key.hprInterval(1.5, (0, 90, 360)).loop()
