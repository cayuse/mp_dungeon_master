from panda3d.core import *
from .myPan.myPan import base
from panda3d.core import GeoMipTerrain, Filename, Material, Texture, TextureStage, NodePath, PandaNode
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
        self.terrainNode = NodePath(PandaNode("TerrainNode"))
        self.terrainNode.reparentTo(base.render)
        self.terrain = GeoMipTerrain("mySimpleTerrain")
        self.terrain.setHeightfield(Filename("terrains/ramp_HM.png"))
        self.terrain.setColorMap(Filename("terrains/red-rock.jpg"))  # pjb comment this line out if you want to set texture directly
        #myTexture = loader.loadTexture("terrains/red-rock.jpg") #pjb UNcomment this line out if you want to set texture directly
        #ts1 = TextureStage('ts')
        #self.terrain.getRoot().setTexture(ts1, myTexture)
        #self.terrain.reparentTo(self.terrainNode)
        self.terrain.setBlockSize(32)
        self.terrain.setBruteforce(True)
        # self.terrain.setNear(40)
        # self.terrain.setFar(100)
        self.terrain.setFocalPoint(base.camera)
        self.root = self.terrain.getRoot()
        self.root.reparentTo(self.terrainNode)
        self.root.setSz(12)
        self.time = 0
        self.elapsed = 0
        #self.root.reparentTo(base.render)
        self.terrain.generate()

        self.roof = base.loader.loadModel("terrains/roof.egg")
        self.roof.setPosHprScale(0,257,18,0,180,0,1,1,1)
        #self.box.setScale(2)
        #self.box.setColor(1,1,0)
        rooftex = base.loader.loadTexture("terrains/roof_TM.png")
        self.roof.setTexture(rooftex, 1)
        self.myMaterial = Material()
        self.myMaterial.setShininess(0.0)  # Make this material shiny
        #self.myMaterial.setAmbient((0, 1, 0, 1))  # Make this material blue
        self.myMaterial.setEmission((0, 0.2, 0, 1))
        self.roof.setMaterial(self.myMaterial)  # Apply the material to this nodePath
        self.roof.reparentTo(self.terrainNode)
        self.pattern = loader.loadTexture('vfx/target.png')
        self.pattern.setWrapU(Texture.WM_clamp)
        self.pattern.setWrapV(Texture.WM_clamp)
        self.targetMarker = NodePath(PandaNode("targetMarker"))
        # self.targetMarker.setPos(122, 175, 0)
        self.targetMarker.reparentTo(base.render)
        self.proj = base.render.attachNewNode(LensNode('proj'))
        self.lens = PerspectiveLens()
        self.proj.node().setLens(self.lens)
        self.proj.reparentTo(self.targetMarker)
        self.proj.setPos(0, 0, 0)
        self.proj.setHpr(0, -90, 0)
        # the next couple of lines are useful to position the projection
        '''self.proj.node().showFrustum()
        self.proj.find('frustum').setColor(1, 0, 0, 1)
        self.camModel = loader.loadModel('camera.egg')
        self.camModel.reparentTo(self.proj)
        self.camModel.setPos(0,0,0)
        '''
        self.ts = TextureStage('ts')
        self.ts.setSort(1)
        self.ts.setMode(TextureStage.MDecal)
        self.root.projectTexture(self.ts, self.pattern, self.proj)

        #the following will add a second projection, it isn't really necessary, just testing if it's psosible
        '''
        self.pattern2 = loader.loadTexture('vfx/plasm2.png')
        self.pattern2.setWrapU(Texture.WM_clamp)
        self.pattern2.setWrapV(Texture.WM_clamp)
        self.ts2 = TextureStage('ts2')
        self.ts2.setSort(1)
        self.ts2.setMode(TextureStage.MDecal)
        self.proj2 = base.render.attachNewNode(LensNode('proj2'))
        self.lens2=PerspectiveLens()
        self.proj2.node().setLens(self.lens2)
        self.proj2.reparentTo(self.targetMarker)
        self.proj2.setPos(0,0,0)
        self.proj2.setHpr(0,-90,0)
        self.root.projectTexture(self.ts2, self.pattern2, self.proj2)
        #self.root.setTexScale(ts1,10,10)
        #self.root.setTexPos(ts1,122,175,.1)
        #self.root.setTexture(ts1, pattern)
        '''
        # projectile
        #self.emptyFire = NodePath("EmptyFire")
        # self.root.setTexture(myTexture) #pjb UNcomment this line out if you want to set texture directly
        # taskMgr.doMethodLater(5, self.updateTerrain, 'Update the Terrain')
        # taskMgr.add(self.updateTerrain, "update")
    def setProjectorPos(self, pos):
        self.targetMarker.setPos(pos)
        #print("mark" + str(self.targetMarker.getPos(base.render)) + "cam" + str(self.proj.getPos(base.render)))
    def setProjectorHpr(self, hpr):
        self.targetMarker.setHpr(hpr)
    def updateTerrain(self, task):
        self.elapsed = base.globalClock.getDt()
        self.time += self.elapsed
        if (self.time > 5):
            self.terrain.update()
            self.time = 0
        return Task.again
