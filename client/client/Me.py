from .myPan.myPan import base, playerScale, playerSpeed
from direct.showbase.DirectObject import DirectObject
from .Projectile import Projectile
# import direct.directbase.DirectStart
from panda3d.core import *
from panda3d.core import Texture
from panda3d.core import WindowProperties, Point3, Vec3, BitMask32, NodePath, AnimControl
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
        self.charNode = NodePath(PandaNode("CharacterNode"))
        self.charNode.reparentTo(base.render)
        self.charNode.setPos(122,175,0)

        self.model = Actor("models/pc/male2",
                           {"strafe": "models/pc/male2_strafe",
                            "attack": "models/pc/male2_attack",
                            "walk": "models/pc/male2_walk"})

        # self.actorHead = self.model.exposeJoint(None, 'modelRoot', 'Joint8')
        # self.model.setScale(4)
        self.playernum = None
        self.timeSinceLastUpdate = 0
        self.model.setScale((playerScale, playerScale, playerScale))
        self.model.reparentTo(self.charNode)
        # self.model.setScale(.01)
        self.isMoving = False
        self.AnimControl = self.model.getAnimControl('walk')
        # self.AnimControl.setPlayRate(0.05)
        self.model.setBlend(frameBlend=1)
        # start position
        # stream = file('models/start.yaml', 'r')
        # start = load(stream)
        # start = load('models/start.yaml', Loader=Loader)
        self.model.setPos(0, 0, 0)
        # STORE TERRAIN SCALE FOR LATER USE#
        self.terrainScale = terrainClass.terrain.getRoot().getSz()
        base.camera.reparentTo(self.charNode)
        self.cameraTargetHeight = 3.0
        # How far should the camera be from Model
        self.cameraDistance = 10
        # Initialize the pitch of the camera
        self.cameraPitch = 10
        self.username = "cayuse"
        self.camDummy = self.charNode.attachNewNode("camDummy")
        self.camDummy.setZ(10)
        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        self.canFire = True
        self.orbitRing = NodePath("orbitRing")
        self.orbitRing.reparentTo(self.charNode)
        self.orbitRing.setPos(0, -10, 0)
        #self.orbitRing.setHpr(0,0,90)
        self.myTarget = NodePath(PandaNode("myTarget"))
        self.myTarget.reparentTo(self.orbitRing)
        #self.myTarget.setPos(self.model.getX()+3,self.model.getY(), self.model.getZ())
        terrainClass.setProjectorPos(self.myTarget.getPos(base.render)+Vec3(0,0,8))


    def setPlayerNum(self, int):
        self.playernum = int


    def resetPlayer(self, task):
        if not self.isMoving:
            self.model.pose("walk", 5)
        else:
            self.model.loop("walk")
        return task.done

    def move(self, keyClass, terrainClass):
        speed = playerSpeed
        # self.meTerrainHeight = terrainClass.terrain.getElevation(self.model.getX(),self.model.getY()) * self.terrainScale
        # self.camTerrainHeight = terrainClass.terrain.getElevation(camera.getX(),camera.getY()) * self.terrainScale
        self.elapsed = globalClock.getDt()
        # base.camera.lookAt(self.actorHead)
        if keyClass.keyMap["left"] != 0:
            self.charNode.setX(self.charNode, (self.elapsed * speed))
            print("me " + str(self.charNode.getPos(base.render)) + "tgt " + str(self.myTarget.getPos(base.render)))
            #print("me"+str(self.model.getX()), str(self.model.getY()), str(self.model.getZ()))
            #print("tgt"+str(self.myTarget.getX()), str(self.myTarget.getY()), str(self.myTarget.getZ()))
            #print(str(self.model.getH()), str(self.model.getP()), str(self.model.getR()))
        if keyClass.keyMap["right"] != 0:
            self.charNode.setX(self.charNode, -(self.elapsed * speed))
        if keyClass.keyMap["forward"] != 0:
            self.charNode.setY(self.charNode, -(self.elapsed * speed))
        if keyClass.keyMap["back"] != 0:
            self.charNode.setY(self.charNode, (self.elapsed * speed))
        #  FIRE
        if keyClass.keyMap["fire1"] == 1:
            #print(self.canFire, len(locals()), len(globals()))
            if self.canFire:
                self.model.play("attack")
                taskMgr.remove('attack_reset')
                taskMgr.doMethodLater(0.5, self.resetPlayer, 'attack_reset')
                self.fireFire(terrainClass)
            self.canFire = False

        if keyClass.keyMap["fire1"] == 0:
            self.canFire = True

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
        myX=self.charNode.getX()
        myY=self.charNode.getY()
        myZ=self.terrainHeight(myX,myY, terrainClass)
        self.charNode.setZ(myZ)
        #self.myTarget.setPos(3, 3, self.terrainHeight(self.myTarget.getZ()+2)  # adjustable later, not sure if there should be defaults
        #self.myTarget.setPos(myX+10, myY, self.terrainHeight(myX+10,myY,terrainClass)+8)
        myX=self.myTarget.getX(base.render)
        myY=self.myTarget.getY(base.render)
        myZ=self.terrainHeight(myX, myY, terrainClass)
        self.orbitRing.setZ(myZ)
        #self.myTarget.setZ(self.terrainHeight(myX, myY, terrainClass))
        #print("model"+str(self.model.getPos()) + "target" + str(self.myTarget.getPos(base.render)) + "orbit" + str(self.orbitRing.getPos(base.render)))
        #terrainClass.setProjectorPos((myX, myY, myZ))
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
            self.charNode.setH(self.charNode.getH() - 0.3 * deltaX)
            #self.myTarget.setR(self.model.getR())
            #self.myTarget.setH(self.model.getH())
            self.orbitRing.setH(base.camera.getH()+90)
            #terrainClass.setProjectorPos(self.myTarget.getPos(base.render)+Vec3(0,0,8))
            terrainClass.setProjectorPos((myX, myY, myZ+6))
            # find the new camera pitch and clamp it to a reasonable range
            self.cameraPitch = self.cameraPitch + 0.1 * deltaY
            if self.cameraPitch < -60: self.cameraPitch = -60
            if self.cameraPitch > 80: self.cameraPitch = 80
            #print(str(self.cameraPitch))
            base.camera.setHpr(0, self.cameraPitch, 0)
            # set the camera at around model's middle
            # We should pivot around here instead of the view target which is noticebly higher
            base.camera.setPos(0, 0, self.cameraTargetHeight / 2)
            # back the camera out to its proper distance
            base.camera.setY(base.camera, self.cameraDistance)
            viewTarget = Point3(0, 0, self.cameraTargetHeight)
            base.camera.lookAt(viewTarget)

        return Task.cont

    def terrainHeight(self,x,y, terrainClass):
        return terrainClass.terrain.getElevation(x,y) * self.terrainScale

    def fireFire(self, terrainClass):
        #self.model.pose("walk", 5)
        startPos = Vec3(self.charNode.getX(), self.charNode.getY(), self.charNode.getZ() + 4)
        myX = self.myTarget.getX(base.render)
        myY = self.myTarget.getY(base.render)
        myZ = self.terrainHeight(myX,myY, terrainClass)
        #print(str(myX),str(myY),str(myZ))
        self.fireNode=Projectile()
        self.fireNode.trajectory(startPos=startPos, endPos=Vec3(myX,myY,myZ), duration=1)

        #p = ParticleEffect()
        #p.loadConfig("particles/fireball.ptf")
        #p.start(parent=self.emptyFire, renderParent=base.render)
        # setup the projectile interval
        #self.fireNode.setDead()
        return Task.cont
