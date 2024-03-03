from .myPan.myPan import base
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from panda3d.core import WindowProperties, Point3, Vec3, BitMask32, NodePath
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionNode, CollisionSphere
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
# from direct.interval.ProjectileInterval import ProjectileInterval
from direct.interval import ProjectileInterval

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


class Projectile(PandaNode):
    def __init__(self, model='vfx/vfx2', texture='vfx/plasm2.png'):
        self.myNode = NodePath(PandaNode("empty_node"))
        self.myNode.setPosHpr(Vec3(0, 0, 0), Vec3(0, 0, 0))
        self.myNode.reparentTo(base.render)
        self.myModel = loader.loadModel(model)
        self.myModel.setTexture(TextureStage.getDefault(), loader.loadTexture(texture), 1)
        self.myModel.reparentTo(self.myNode)
        self.myModel.setLightOff()
        self.myModel.setHpr(0, 0, 0)
        self.myModel.setHpr(-90, 0, 0)  # adjustable later, not sure if these should be here or required on calling
        self.myModel.setPos(0, 0, 0)  # adjustable later, not sure if there should be defaults
        #self.myPointLight = PointLight('myPointLight')
        #self.myPointLight.setColor((1, 1, 1, 1))  # again, maybe should be part of calling convention
        #self.myPointLight.attenuation = (0, 0, 1)
        #self.myPointLight.reparentTo(self.myNode)
        #self.point_light_node = base.render.attachNewNode(self.myPointLight)
        #self.point_light_node.reparentTo(self.myNode)
        #self.point_light_node.setPos(0, 0, 0)  # relative to MyPoint
        #render.setLight(self.point_light_node)
        #self.point
        self.vfxU = 0
        self.vfxV = 0
        self.down = True
        self.sum_oper = operator.add
        # self.start()
        self.isAlive = False

    def trajectory(self, startPos, endPos, duration=1):
        self.myTraj = ProjectileInterval.ProjectileInterval(self.myNode, startPos,endPos=endPos, duration=duration)
        self.myTraj.start()
        self.start("vfx")

    def setDead(self):
        self.isAlive = False

    def setModelHpr(self, hpr=(-90, 0, 0)):  # model hpr relative to base node
        self.myModel.setHpr(hpr)

    def setModelPos(self, pos=(0, 0, 0)):  # model pos relative to base node
        self.myModel.setPos(pos)

    def setLightColor(self, color=(1, 1, 1, 1)):
        self.myPointLight.setColor(color)

    def start(self, task, speed=0.015):
        taskMgr.doMethodLater(speed, self.runAnimation, task)

    def runAnimation(self, task):
        self.myNode.lookAt(base.camera)
        self.myModel.setTexOffset(TextureStage.getDefault(), self.vfxU * 0.125,
                                  self.vfxV * -0.125)  # starting state = 0,0
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
        if self.vfxV >= 8:
            self.vfxV = 7
            self.down = not self.down
        if self.myTraj.isStopped():
            self.myNode.removeNode()
            return task.done
        return task.again
