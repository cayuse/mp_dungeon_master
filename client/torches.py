from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
base.enableParticles()
from direct.particles.ParticleEffect import ParticleEffect
import sys

class Torches(DirectObject):
    def __init__(self):
        torches = [(  154.0 ,  241.5  ),
(  129.5 ,  217.5  ),
(  90.5 ,  232.0  ),
(  79.0 ,  175.0  ),
(  92.0 ,  87.0  ),
(  127.0 ,  82.5  ),
(  119.0 ,  146.0  ),
(  147.5 ,  24.0  ),
(  29.5 ,  208.5  ),
(  147.5 ,  188.0  ),
(  200.0 ,  238.5  ),
(  197.5 ,  80.5  ),
(  31.0 ,  120.5  ),
(  239.0 ,  26.5  ),
(  61.0 ,  21.5  ),
(  31.0 ,  35.5  ),
(  82.5 ,  146.0  ),
(  152.0 ,  140.0  ),
(  159.0 ,  215.0  ),
(  163.0 ,  102.0  ),
(  58.5 ,  212.0  ),
(  198.5 ,  164.5  ),
(  206.0 ,  39.5  ),
(  104.0 ,  115.5  ),
(  241.0 ,  57.0  ),
(  240.5 ,  102.5  ),
(  176.5 ,  15.5  ),
(  104.5 ,  22.0  ),
(  186.5 ,  198.5  ),
(  44.0 ,  80.0  ),
(  231.0 ,  187.0  ),
(  28.0 ,  166.0  ),
(  197.5 ,  129.5  ),
(  162.0 ,  69.0  ),
(  62.5 ,  47.5  ),
(  131.0 ,  107.5  ),
(  230.0 ,  140.0  ),
(  77.0 ,  119.0  )]
        tex = loader.loadTexture("models/rocks.jpg")
        for torch in torches:
            x = torch[1]
            y = 256-torch[0]
            self.torch = loader.loadModel("models/wall-torch")
            self.torch.setTexture(tex,1)
            self.torch.reparentTo(render)
            self.torch.setPosHprScale(x,y,8,0,90,0,0.1,0.1,0.1)
            p = ParticleEffect()
            p.loadConfig("particles/fireish.ptf")
            p.start(parent=self.torch, renderParent=render)

            plight = PointLight('plight')
            plight.setColor(Vec4(255, 255, 255, 1))
            plnp = render.attachNewNode(plight)
            plnp.setPos(Vec3(x,y, 9))
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
