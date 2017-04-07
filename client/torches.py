from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
base.enableParticles()
from direct.particles.ParticleEffect import ParticleEffect
import sys
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class Torches(DirectObject):
    def __init__(self):
        stream = file('models/torches.yaml', 'r')
        torches = load(stream)
        tex = loader.loadTexture("models/rocks.jpg")
        for torch in torches:
            x = torch[1]
            y = 256-torch[0]
            self.torch = loader.loadModel("models/wall-torch")
            self.torch.setTexture(tex,1)
            self.torch.reparentTo(render)
            self.torch.setPosHprScale(x, y, 7, 0, 90, 0, 0.1, 0.1, 0.1)
            p = ParticleEffect()
            p.loadConfig("particles/fireish.ptf")
            p.start(parent=self.torch, renderParent=render)

            plight = PointLight('plight')
            plight.setColor(Vec4(50, 40, 10, 1))
            plnp = render.attachNewNode(plight)
            plnp.setPos(Vec3(x,y, 7))
            plight.setAttenuation((1, 0, 0.5))
            render.setLight(plnp)
            #plnp = lightpivot.attachNewNode(plight)
            #self.torch.setShaderAuto()

            '''
            slight = Spotlight('slight')
            slight.setColor(Vec4(30, 15, 5, 1))
            lens = PerspectiveLens()
            slight.setLens(lens)
            slnp = render.attachNewNode(slight)
            slnp.setPos(182,192, 11)
            slnp.setHpr(0, 90, 0)
            #slnp.lookAt(myObject)
            render.setLight(slnp)
            '''
