from .myPan.myPan import base, playerScale, playerSpeed
from direct.showbase.DirectObject import DirectObject
# import direct.directbase.DirectStart
from panda3d.core import *
from panda3d.core import WindowProperties, Point3, Vec3, BitMask32, NodePath
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionNode, CollisionSphere
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.interval.ProjectileInterval import ProjectileInterval
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.gui.DirectGui import *
from direct.interval import ProjectileInterval
import operator

base.enableParticles()
from direct.particles.ParticleEffect import ParticleEffect
from .vfx import vfx, MovingVfx
import sys

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Me(DirectObject):
    def __init__(self, terrainClass):

        '''
        self.model = Actor("models/pc/female_nude", {"attack1": "models/pc/female_attack1",
                                                     "attack2": "models/pc/female_attack2",
                                                     "walk": "models/pc/female_run",
                                                     "die": "models/pc/female_die",
                                                     "strafe": "models/pc/female_strafe",
                                                     "hit": "models/pc/female_hit",
                                                     "idle": "models/pc/female_idle"})
        '''
        self.model = Actor("models/wiz/male2",
                           {"strafe": "models/wiz/male2_strafe",
                            "walk": "models/wiz/male2_walk"})

        # self.actorHead = self.model.exposeJoint(None, 'modelRoot', 'Joint8')
        # self.model.setScale(4)
        self.playernum = None
        self.timeSinceLastUpdate = 0
        self.model.setScale((0.1, 0.1, 0.1))
        self.model.reparentTo(base.render)
        # self.model.setScale(.01)
        self.isMoving = False
        self.AnimControl = self.model.getAnimControl('walk')
        # self.AnimControl.setPlayRate(0.05)
        self.model.setBlend(frameBlend=1)
        # start position
        # stream = file('models/start.yaml', 'r')
        # start = load(stream)
        # start = load('models/start.yaml', Loader=Loader)
        self.model.setPos(122, 175, 0)
        # STORE TERRAIN SCALE FOR LATER USE#
        self.terrainScale = terrainClass.terrain.getRoot().getSz()
        base.camera.reparentTo(self.model)
        self.cameraTargetHeight = 3.0
        # How far should the camera be from Model
        self.cameraDistance = 500
        # Initialize the pitch of the camera
        self.cameraPitch = 10
        self.username = "cayuse"
        self.camDummy = self.model.attachNewNode("camDummy")
        self.camDummy.setZ(10)
        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        # projectile
        #self.emptyFire = NodePath("EmptyFire")
        self.fireNode = NodePath(PandaNode("empty_node"))
        self.fireNode.set_pos_hpr(0,0,0,0,0,0)
        self.fireNode.reparentTo(base.render)
        self.emptyFire = loader.loadModel('vfx/vfx2')
        self.emptyFire.setTexture(TextureStage.getDefault(), loader.loadTexture("vfx/plasm2.png"), 1)
        self.emptyFire.reparentTo(self.fireNode)
        self.emptyFire.setLightOff()
        self.emptyFire.setHpr(0,0,0)
        self.emptyFire.setHpr(-90, 0, 0)
        self.emptyFire.setPos(0,0,0)
        #self.emptyFire.lookAt(base.camera)
        #self.emptyFire.loop(0.015)
        self.point_light = PointLight('point_light')
        self.point_light.setColor((1, 1, 1, 1))
        self.point_light_node = base.render.attachNewNode(self.point_light)
        self.point_light_node.reparentTo(self.fireNode)
        self.point_light_node.setPos(0, 0, 0)
        base.render.setLight(self.point_light_node)
        self.vfxU = 0
        self.vfxV = 0
        self.down = True
        self.sum_oper = operator.add
        self.start()

    def updateVfxV(self):
        pass

    def start(self, speed=0.04):
        taskMgr.doMethodLater(speed, self.run, 'vfx')
    def run(self, task):
        self.fireNode.lookAt(base.camera)
        self.emptyFire.setTexOffset(TextureStage.getDefault(), self.vfxU*0.125, self.vfxV*-0.125) #starting state = 0,0
        if self.down:
            self.sum_oper = operator.add
        else:
            self.sum_oper = operator.sub
        self.vfxU = self.sum_oper(self.vfxU, 1)
        if self.vfxU >= 8.0:
            if self.vfxV == 7:
                self.vfxU = 7
            else:
                self.vfxU = 0
            self.vfxV = self.sum_oper(self.vfxV, 1)
        if self.vfxU < 0:
            if self.vfxV == 0:
                self.vfxU = 0
            else:
                self.vfxU = 7
            self.vfxV = self.sum_oper(self.vfxV, 1)
        if self.vfxV < 0:
            self.vfxV = 0
            self.down = not self.down
        if self.vfxV >=8:
            self.vfxV = 7
            self.down = not self.down

        '''
        self.vfxU = vfxU_oper(self.vfxU,0.125)
        #self.vfxU=0.5
        if self.vfxU >= 1.0 or self.vfxU == 0:
            if self.down:
                self.vfxU=0
            else:
                self.ufxU=1.0
            self.vfxV = vfxV_oper(self.vfxV,0.125)
        if self.vfxV <=-1 or self.vfxV > 0:
            print("reversed")
            self.vfxV=vfxU_oper(self.vfxU,0.125)
            self.down = not self.down
            #self.emptyFire.removeNode()
            #return task.done
        '''
        #self.fireNode.lookAt(base.camera)
        #self.emptyFire.setTexOffset(TextureStage.getDefault(), self.vfxU, self.vfxV)
        #print(str(self.vfxU) + " " + str(self.vfxV))
        #print(str(self.emptyFire.getHpr()), str(self.fireNode.getHpr()))
        return task.again
    def setPlayerNum(self, int):
        self.playernum = int


    def move(self, keyClass, terrainClass):
        speed = playerSpeed
        # self.meTerrainHeight = terrainClass.terrain.getElevation(self.model.getX(),self.model.getY()) * self.terrainScale
        # self.camTerrainHeight = terrainClass.terrain.getElevation(camera.getX(),camera.getY()) * self.terrainScale
        self.elapsed = globalClock.getDt()
        # base.camera.lookAt(self.actorHead)
        if (keyClass.keyMap["left"] != 0):
            self.model.setX(self.model, (self.elapsed * speed))
            #print(str(self.model.getX()), str(self.model.getY()), str(self.model.getZ()))
            print(str(self.model.getH()), str(self.model.getP()), str(self.model.getR()))
        if (keyClass.keyMap["right"] != 0):
            self.model.setX(self.model, -(self.elapsed * speed))
        if (keyClass.keyMap["forward"] != 0):
            self.model.setY(self.model, -(self.elapsed * speed))
        if (keyClass.keyMap["back"] != 0):
            self.model.setY(self.model, (self.elapsed * speed))
        #  FIRE
        if (keyClass.keyMap["fire1"] != 0):
            self.fireFire(terrainClass)

        if (keyClass.keyMap["forward"] != 0) or (keyClass.keyMap["back"]):
            if self.isMoving is False:
                self.model.loop("walk")
                self.isMoving = True
        elif (keyClass.keyMap["left"] != 0) or (keyClass.keyMap["right"] != 0):
            if self.isMoving is False:
                self.model.loop("strafe")
                self.isMoving = True
        else:
            if self.isMoving:
                self.model.stop()
                self.model.pose("walk", 5)
                self.isMoving = False

        self.meTerrainHeight = terrainClass.terrain.getElevation(self.model.getX(),
                                                                 self.model.getY()) * self.terrainScale
        self.model.setZ(self.meTerrainHeight)

        # CAMERA CONTROL#
        if base.mouseWatcherNode.hasMouse():
            # get changes in mouse position
            md = base.win.getPointer(0)
            x = md.getX()
            y = md.getY()
            deltaX = md.getX() - 200
            deltaY = md.getY() - 200
            # reset mouse cursor position
            base.win.movePointer(0, 200, 200)
            # alter model's yaw by an amount proportionate to deltaX
            self.model.setH(self.model.getH() - 0.3 * deltaX)
            # find the new camera pitch and clamp it to a reasonable range
            self.cameraPitch = self.cameraPitch + 0.1 * deltaY
            if self.cameraPitch < -60: self.cameraPitch = -60
            if self.cameraPitch > 80: self.cameraPitch = 80
            base.camera.setHpr(0, self.cameraPitch, 0)
            # set the camera at around model's middle
            # We should pivot around here instead of the view target which is noticebly higher
            base.camera.setPos(0, 0, self.cameraTargetHeight / 2)
            # back the camera out to its proper distance
            base.camera.setY(base.camera, self.cameraDistance)
            viewTarget = Point3(0, 0, self.cameraTargetHeight)
            base.camera.lookAt(viewTarget)

        return Task.cont

    def fireFire(self, terrainClass):
        startPos = Vec3(self.model.getX(), self.model.getY(), self.model.getZ() + 2)
        self.fireNode.setPos(startPos)
        #p = ParticleEffect()
        #p.loadConfig("particles/fireball.ptf")
        #p.start(parent=self.emptyFire, renderParent=base.render)
        # setup the projectile interval
        self.trajectory = ProjectileInterval.ProjectileInterval(self.fireNode, startPos=startPos,
                                                                endPos=Vec3(122, 175, 0), duration=1)
        self.trajectory.start()
        return Task.cont
