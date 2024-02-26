from panda3d.core import *
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


class Terrain(GeoMipTerrain):
    def __init__(self):
        self.terrain = GeoMipTerrain("mySimpleTerrain")
        self.terrain.setHeightfield(Filename("terrains/ramp_HM.png"))
        self.terrain.setColorMap(
            Filename("terrains/red-rock.jpg"))  # pjb comment this line out if you want to set texture directly
        # myTexture = loader.loadTexture("terrain.bmp") #pjb UNcomment this line out if you want to set texture directly

        self.terrain.setBlockSize(32)
        self.terrain.setBruteforce(True)
        # self.terrain.setNear(40)
        # self.terrain.setFar(100)
        self.terrain.setFocalPoint(base.camera)
        self.terrain.getRoot().setSz(12)
        self.time = 0
        self.elapsed = 0
        self.terrain.getRoot().reparentTo(render)
        self.terrain.generate()

        self.roof = loader.loadModel("terrains/roof.egg")
        self.roof.setPosHprScale(0,257,18,0,180,0,1,1,1)
        #self.box.setScale(2)
        #self.box.setColor(1,1,0)
        rooftex = loader.loadTexture("terrains/roof_TM.png")
        self.roof.setTexture(rooftex, 1)
        self.myMaterial = Material()
        self.myMaterial.setShininess(0.0)  # Make this material shiny
        #self.myMaterial.setAmbient((0, 1, 0, 1))  # Make this material blue
        self.myMaterial.setEmission((0, 0.2, 0, 1))
        self.roof.setMaterial(self.myMaterial)  # Apply the material to this nodePath
        self.roof.reparentTo(render)
        # self.terrain.getRoot().setTexture(myTexture) #pjb UNcomment this line out if you want to set texture directly
        # taskMgr.doMethodLater(5, self.updateTerrain, 'Update the Terrain')
        # taskMgr.add(self.updateTerrain, "update")
    def updateTerrain(self, task):
        self.elapsed = globalClock.getDt()
        self.time += self.elapsed
        if (self.time > 5):
            self.terrain.update()
            self.time = 0
        return Task.again

