from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
base.enableParticles()
from direct.particles.ParticleEffect import ParticleEffect
import sys

class Torches(DirectObject):
    def __init__(self):
        torches = [(  42.5 ,  159.0  ),
(  62.0 ,  123.0  ),
(  91.0 ,  85.0  ),
(  159.5 ,  106.0  ),
(  78.5 ,  172.0  ),
(  191.5 ,  229.5  ),
(  85.0 ,  114.0  ),
(  198.0 ,  82.0  ),
(  225.0 ,  19.0  ),
(  209.5 ,  123.0  ),
(  126.0 ,  47.5  ),
(  138.0 ,  162.5  ),
(  180.5 ,  173.0  ),
(  27.0 ,  37.0  ),
(  171.0 ,  33.5  ),
(  201.5 ,  202.0  ),
(  34.0 ,  86.5  ),
(  127.0 ,  226.5  ),
(  29.0 ,  202.5  ),
(  84.0 ,  40.0  ),
(  83.5 ,  222.0  ),
(  132.5 ,  81.5  ),
(  55.5 ,  236.5  ),
(  235.0 ,  74.5  ),
(  15.0 ,  165.0  ),
(  125.5 ,  127.0  ),
(  235.5 ,  191.0  ),
(  20.5 ,  131.0  ),
(  139.5 ,  12.5  ),
(  136.5 ,  189.0  ),
(  74.0 ,  13.5  ),
(  158.5 ,  218.5  ),
(  228.5 ,  165.0  ),
(  205.5 ,  167.0  ),
(  168.5 ,  77.5  ),
(  215.0 ,  239.5  )]
        tex = loader.loadTexture("models/rocks.jpg")
        for torch in torches:
            self.torch = loader.loadModel("models/wall-torch")
            self.torch.setTexture(tex,1)
            self.torch.reparentTo(render)
            self.torch.setPosHprScale(torch[0],torch[1],8,0,90,0,0.1,0.1,0.1)
            p = ParticleEffect()
            p.loadConfig("particles/fireish.ptf")
            p.start(parent=self.torch, renderParent=render)

            plight = PointLight('plight')
            plight.setColor(Vec4(255, 255, 255, 1))
            plnp = render.attachNewNode(plight)
            plnp.setPos(Vec3(257-torch[1],257-torch[0], 9))
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
