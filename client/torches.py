from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
base.enableParticles()
from direct.particles.ParticleEffect import ParticleEffect
import sys

class Torches(DirectObject):
    def __init__(self):
        torches = [(  197.0 ,  240.0  ),
(  117.0 ,  85.0  ),
(  52.0 ,  159.5  ),
(  33.5 ,  35.0  ),
(  153.5 ,  212.5  ),
(  101.0 ,  221.5  ),
(  37.5 ,  118.5  ),
(  69.0 ,  17.0  ),
(  175.0 ,  27.0  ),
(  45.0 ,  216.5  ),
(  198.5 ,  147.0  ),
(  205.5 ,  86.5  ),
(  241.0 ,  89.0  ),
(  23.0 ,  195.5  ),
(  128.0 ,  40.5  ),
(  98.0 ,  176.0  ),
(  52.5 ,  74.5  ),
(  22.5 ,  69.0  ),
(  212.5 ,  198.0  ),
(  88.5 ,  127.0  ),
(  122.5 ,  136.0  ),
(  162.5 ,  83.5  ),
(  236.5 ,  52.0  ),
(  233.0 ,  138.5  ),
(  9.0 ,  150.0  ),
(  76.0 ,  101.0  ),
(  230.5 ,  19.0  ),
(  170.5 ,  175.5  ),
(  136.0 ,  170.0  ),
(  158.5 ,  121.0  ),
(  77.5 ,  205.0  ),
(  37.0 ,  10.0  ),
(  43.5 ,  187.5  )]
        tex = loader.loadTexture("models/rocks.jpg")
        for torch in torches:
            self.torch = loader.loadModel("models/wall-torch")
            self.torch.setTexture(tex,1)
            self.torch.reparentTo(render)
            self.torch.setPosHprScale(torch[0],257-torch[1],8,0,90,0,0.1,0.1,0.1)
            p = ParticleEffect()
            p.loadConfig("particles/fireish.ptf")
            p.start(parent=self.torch, renderParent=render)

            plight = PointLight('plight')
            plight.setColor(Vec4(255, 255, 255, 1))
            plnp = render.attachNewNode(plight)
            plnp.setPos(Vec3(torch[0],257-torch[1], 9))
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
