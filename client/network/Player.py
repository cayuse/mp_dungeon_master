from direct.showbase.DirectObject import DirectObject

class Player(DirectObject):
    def __init__(self):
        self.currentPos = {'x': 244, 'y': 188, 'z': 0, 'h': 0, 'p': 0, 'r': 0}  # stores rotation too
        self.isMoving = False
        self.username = ""

    def load(self):
        self.model = Actor("models/ralph",
                           {"run": "models/ralph-run",
                            "walk": "models/ralph-walk"})
        self.model.reparentTo(render)
        self.model.setScale(0.5)
        self.isMoving = False
        self.AnimControl = self.model.getAnimControl('walk')
        self.AnimControl.setPlayRate(0.05)
        self.model.setBlend(frameBlend=1)