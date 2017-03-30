from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
base.enableParticles()
from direct.particles.ParticleEffect import ParticleEffect
import sys

class Torches(DirectObject):  # This class will regulate the players
    def __init__(self):
        torches = [ (  122.5 ,  213.5  ),
(  150.0 ,  136.0  ),
(  91.0 ,  138.0  ),
(  197.0 ,  79.0  ),
(  180.5 ,  35.5  ),
(  237.5 ,  12.0  ),
(  30.5 ,  111.5  ),
(  171.5 ,  189.0  ),
(  209.0 ,  169.0  ),
(  93.0 ,  178.5  ),
(  123.5 ,  93.0  ),
(  82.0 ,  24.0  ),
(  233.0 ,  99.5  ),
(  119.0 ,  28.0  ),
(  50.0 ,  224.5  ),
(  75.0 ,  79.0  ),
(  224.0 ,  236.5  ),
(  24.5 ,  47.0  ),
(  193.5 ,  131.5  ),
(  237.0 ,  160.0  ),
(  29.0 ,  158.5  ),
(  154.5 ,  237.0  ),
(  34.0 ,  193.5  ),
(  239.0 ,  199.5  ),
(  45.0 ,  16.5  ),
(  163.5 ,  84.5  ),
(  138.0 ,  167.0  ),
(  230.5 ,  53.5  )]
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
            self.torch.setShaderInput("light", plnp)

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
