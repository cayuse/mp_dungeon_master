from client.myPan.myPan import base
#import direct.directbase.DirectStart
#from direct.showbase.DirectObject import DirectObject
#from direct.task.Task import Task

#from direct.distributed.PyDatagram import PyDatagram
#from direct.distributed.PyDatagramIterator import PyDatagramIterator
#from direct.actor.Actor import Actor
from client import Client, Keys, Me, Terrain, chatRegulator
from client.network import World, PlayerReg
from torches import *
from goldenkeys import *
#from network import *
from MapObjects import *
import sys

#Just some groundwork

base.disableMouse()
base.camera.setPos(0,0,10)

#establish connection > send/receive updates > update world
worldClient = Client(9099,"127.0.0.1")
Terrain = Terrain()
N = PlayerReg()
me = Me(Terrain)
keys = Keys()
w = World()
Torches()
GoldenKeys()
chatReg = chatRegulator(worldClient,keys)

print("updating name")
w.UpdateName(me, worldClient)
base.taskMgr.add(N.updatePlayers,"keep every player where they are supposed to be",extraArgs = [me])
base.taskMgr.add(me.move,"move our penguin", extraArgs = [keys,Terrain])
base.taskMgr.add(worldClient.tskReaderPolling,"Poll the connection reader",extraArgs = [me,N,chatReg])
base.taskMgr.add(w.UpdateWorld,"keep the world up to date",extraArgs = [me,worldClient])


#=============================================================================#
#test code for lighting, normal mapping, etc...#
#ambient light
alight = AmbientLight('alight')
alight.setColor(Vec4(0.1, 0.1, 0.1, 0.1))
alnp = base.render.attachNewNode(alight)
base.render.setLight(alnp)
base.render.setShaderAuto()
me.model.setShaderAuto()
#me.model.setNormalMap("models/nskinrd-normal.jpg")


#lightpivot = render.attachNewNode("lightpivot")
#lightpivot.setPos(0,0,25)
#plight = PointLight('plight')
#plight.setColor(Vec4(1, 1, 1, 1))
#plnp = lightpivot.attachNewNode(plight)
#render.setLight(plnp)
#me.model.setShaderInput("light", plnp)
#=============================================================================#
#Castle = Castle(Vec3(288.96,294.45,30.17), Vec3(119.05,270,0),0.08)
base.run()

