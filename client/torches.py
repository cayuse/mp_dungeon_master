from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
base.enableParticles()
from direct.particles.ParticleEffect import ParticleEffect
import sys

class Torches(DirectObject):
    def __init__(self):
        torches = [(  167.5 ,  126.5  ),
(  213.5 ,  117.0  ),
(  149.5 ,  201.0  ),
(  55.5 ,  150.0  ),
(  203.0 ,  169.5  ),
(  119.5 ,  201.5  ),
(  102.5 ,  79.5  ),
(  23.5 ,  51.0  ),
(  231.5 ,  21.5  ),
(  188.0 ,  52.5  ),
(  47.5 ,  226.5  ),
(  74.0 ,  19.0  ),
(  86.0 ,  237.5  ),
(  34.0 ,  100.5  ),
(  81.0 ,  120.0  ),
(  216.5 ,  204.0  ),
(  135.0 ,  114.5  ),
(  88.5 ,  199.0  ),
(  121.5 ,  151.0  ),
(  141.5 ,  22.5  ),
(  206.5 ,  230.0  ),
(  147.0 ,  76.5  ),
(  16.5 ,  230.5  ),
(  148.5 ,  160.0  ),
(  57.0 ,  183.0  ),
(  29.5 ,  149.0  ),
(  153.5 ,  236.5  ),
(  219.0 ,  64.0  ),
(  26.0 ,  180.5  ),
(  236.5 ,  168.0  ),
(  181.0 ,  19.0  )]
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
