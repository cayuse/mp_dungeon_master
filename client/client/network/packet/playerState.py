from direct.showbase.DirectObject import DirectObject
from panda3d.core import LPoint3f
from panda3d.core import LVecBase3f
import pickle

class playerState(DirectObject):
    def __init__(self, PosHpr=(1,2,3,4,5,6)):
        self.type = "state"
        self.PosHpr = PosHpr

class playerAction(DirectObject):
    def __init__(self, action):
        self.type = "action"
        self.action = action