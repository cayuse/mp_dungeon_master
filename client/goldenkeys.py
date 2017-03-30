from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import sys

class GoldenKeys(DirectObject):  # This class will regulate the players
    def __init__(self):
        keys =[ (  122.5 ,  213.5  ),
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
        tex = loader.loadTexture("models/golden-key.tif")
        for key in keys:
            self.key = loader.loadModel("models/golden-key")
            self.key.setTexture(tex,1)
            self.key.reparentTo(render)
            self.key.setPosHprScale(key[0],257-key[1],1,0,90,0,1,1,1)
