from direct.directbase.DirectStart import *
from direct.actor import Actor
from panda3d.core import *

base.setBackgroundColor(1, 1, 1, 1)

ripple = Actor.Actor('ripple.egg')
ripple.reparentTo(render)
ripple.setScale(10)
ripple.pose('animation', 17)

dl = DirectionalLight('dl')
dlnp = camera.attachNewNode(dl)
ripple.setLight(dlnp)

proj = render.attachNewNode(LensNode('proj'))
lens = PerspectiveLens()
proj.node().setLens(lens)
proj.node().showFrustum()
proj.find('frustum').setColor(1, 0, 0, 1)
camModel = loader.loadModel('camera.egg')
camModel.reparentTo(proj)
proj.reparentTo(render)
proj.setPos(1.5, -7.3, 2.9)
proj.setHpr(22, -15, 0)

tex = loader.loadTexture('maps/envir-reeds.png')
tex.setWrapU(SamplerState.WMBorderColor)
tex.setWrapV(SamplerState.WMBorderColor)
tex.setBorderColor((1, 1, 1, 0))
ts = TextureStage('ts')
ts.setSort(1)
ts.setMode(TextureStage.MDecal)
ripple.projectTexture(ts, tex, proj)

base.disableMouse()
camera.setPos(-7.8, -22.4, 0)
camera.setHpr(-21, 0, 0)

base.graphicsEngine.renderFrame()
base.screenshot('projected_bamboo.jpg', defaultFilename=0)