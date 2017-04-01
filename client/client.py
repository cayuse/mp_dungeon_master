from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.gui.DirectGui import *
import sys


class Client(DirectObject):
    def __init__(self, p, i):
        self.cManager = QueuedConnectionManager()  # Manages connections
        self.cReader = QueuedConnectionReader(self.cManager, 0)  # Reads incoming Data
        self.cWriter = ConnectionWriter(self.cManager, 0)  # Sends Data
        self.port = p  # Server's port
        self.ip = i  # server's ip
        self.Connection = self.cManager.openTCPClientConnection(self.ip, self.port, 3000)  # Create the connection
        if self.Connection:
            self.cReader.addConnection(self.Connection)  # receive messages from server
        else:
            print 'connection failed'

    def tskReaderPolling(self, m, playerRegulator,
                         chatClass):  # this function checks to see if there is any data from the server
        if self.cReader.dataAvailable():
            self.datagram = NetDatagram()  # catch the incoming data in this instance
            # Check the return value; if we were threaded, someone else could have
            # snagged this data before we did
            if self.cReader.getData(self.datagram):
                playerRegulator.ProcessData(self.datagram, m, chatClass)
                self.datagram.clear()
        return Task.cont


class Terrain(GeoMipTerrain):
    def __init__(self):
        self.terrain = GeoMipTerrain("mySimpleTerrain")
        self.terrain.setHeightfield(Filename("terrains/ramp_HM.png"))
        self.terrain.setColorMap(
            Filename("terrains/red-rock.jpg"))  # pjb comment this line out if you want to set texture directly
        # myTexture = loader.loadTexture("terrain.bmp") #pjb UNcomment this line out if you want to set texture directly

        self.terrain.setBlockSize(32)
        self.terrain.setBruteforce(True)
        # self.terrain.setNear(40)
        # self.terrain.setFar(100)
        self.terrain.setFocalPoint(base.camera)
        self.terrain.getRoot().setSz(12)
        self.time = 0
        self.elapsed = 0
        self.terrain.getRoot().reparentTo(render)
        self.terrain.generate()

        self.roof = loader.loadModel("terrains/roof.egg")
        self.roof.setPosHprScale(0,257,18,0,180,0,1,1,1)
        #self.box.setScale(2)
        #self.box.setColor(1,1,0)
        rooftex = loader.loadTexture("terrains/roof_TM.png")
        self.roof.setTexture(rooftex, 1)
        self.myMaterial = Material()
        self.myMaterial.setShininess(0.0)  # Make this material shiny
        #self.myMaterial.setAmbient((0, 1, 0, 1))  # Make this material blue
        self.myMaterial.setEmission((0, 0.2, 0, 1))
        self.roof.setMaterial(self.myMaterial)  # Apply the material to this nodePath
        self.roof.reparentTo(render)
        # self.terrain.getRoot().setTexture(myTexture) #pjb UNcomment this line out if you want to set texture directly
        # taskMgr.doMethodLater(5, self.updateTerrain, 'Update the Terrain')
        # taskMgr.add(self.updateTerrain, "update")
    def updateTerrain(self, task):
        self.elapsed = globalClock.getDt()
        self.time += self.elapsed
        if (self.time > 5):
            self.terrain.update()
            self.time = 0
        return Task.again

class Me(DirectObject):
    def __init__(self, terrainClass):

        self.model = Actor("models/ralph",
                           {"run": "models/ralph-run",
                            "walk": "models/ralph-walk"})
        self.actorHead = self.model.exposeJoint(None, 'modelRoot', 'Joint8')
        # self.model.setScale(4)
        self.playernum = None
        self.timeSinceLastUpdate = 0
        self.model.reparentTo(render)
        self.model.setScale(0.5)
        self.isMoving = False
        self.AnimControl = self.model.getAnimControl('walk')
        self.AnimControl.setPlayRate(0.05)
        self.model.setBlend(frameBlend=1)
        #start position
        self.model.setPos(119,179,0)
        # STORE TERRAIN SCALE FOR LATER USE#
        self.terrainScale = terrainClass.terrain.getRoot().getSz()
        base.camera.reparentTo(self.model)
        self.cameraTargetHeight = 3.0
        # How far should the camera be from Model
        self.cameraDistance = 30
        # Initialize the pitch of the camera
        self.cameraPitch = 10

        self.camDummy = self.model.attachNewNode("camDummy")
        self.camDummy.setZ(5)
        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

    def setPlayerNum(self, int):
        self.playernum = int

    def move(self, keyClass, terrainClass):
        speed = 40
        # self.meTerrainHeight = terrainClass.terrain.getElevation(self.model.getX(),self.model.getY()) * self.terrainScale
        # self.camTerrainHeight = terrainClass.terrain.getElevation(camera.getX(),camera.getY()) * self.terrainScale
        self.elapsed = globalClock.getDt()
        # base.camera.lookAt(self.actorHead)
        if (keyClass.keyMap["left"] != 0):
            self.model.setX(self.model, (self.elapsed * speed))
            print str(self.model.getX()), str(self.model.getY()), str(self.model.getZ())
        if (keyClass.keyMap["right"] != 0):
            self.model.setX(self.model, -(self.elapsed * speed))
        if (keyClass.keyMap["forward"] != 0):
            self.model.setY(self.model, -(self.elapsed * speed))
        if (keyClass.keyMap["back"] != 0):
            self.model.setY(self.model, (self.elapsed * speed))

        if (keyClass.keyMap["forward"] != 0) or (keyClass.keyMap["left"] != 0) or (keyClass.keyMap["right"] != 0):
            if self.isMoving is False:
                self.model.loop("walk")
                self.isMoving = True
        else:
            if self.isMoving:
                self.model.stop()
                self.model.pose("walk", 5)
                self.isMoving = False

        self.meTerrainHeight = terrainClass.terrain.getElevation(self.model.getX(),
                                                                 self.model.getY()) * self.terrainScale
        self.model.setZ(self.meTerrainHeight)

        # CAMERA CONTROL#
        if base.mouseWatcherNode.hasMouse():
            # get changes in mouse position
            md = base.win.getPointer(0)
            x = md.getX()
            y = md.getY()
            deltaX = md.getX() - 200
            deltaY = md.getY() - 200
            # reset mouse cursor position
            base.win.movePointer(0, 200, 200)
            # alter model's yaw by an amount proportionate to deltaX
            self.model.setH(self.model.getH() - 0.3 * deltaX)
            # find the new camera pitch and clamp it to a reasonable range
            self.cameraPitch = self.cameraPitch + 0.1 * deltaY
            if (self.cameraPitch < -60): self.cameraPitch = -60
            if (self.cameraPitch > 80): self.cameraPitch = 80
            base.camera.setHpr(0, self.cameraPitch, 0)
            # set the camera at around model's middle
            # We should pivot around here instead of the view target which is noticebly higher
            base.camera.setPos(0, 0, self.cameraTargetHeight / 2)
            # back the camera out to its proper distance
            base.camera.setY(base.camera, self.cameraDistance)
            viewTarget = Point3(0, 0, self.cameraTargetHeight)
            base.camera.lookAt(viewTarget)
        return Task.cont




class Keys(DirectObject):
    def __init__(self):
        self.isTyping = False
        self.keyMap = {"left": 0, "right": 0, "forward": 0, "back": 0, "cam": 0, "right": 0, "autoRun": 0}
        #Quits game
        self.accept("escape", sys.exit)

        self.accept(",", self.setKey, ["forward", 1])
        self.accept(",-up", self.setKey, ["forward", 0])
        self.accept("w", self.setKey, ["forward", 1])
        self.accept("w-up", self.setKey, ["forward", 0])

        self.accept("a", self.setKey, ["left", 1])
        self.accept("a-up", self.setKey, ["left", 0])

        self.accept("o", self.setKey, ["back", 1])
        self.accept("o-up", self.setKey, ["back", 0])
        self.accept("d", self.setKey, ["back", 1])
        self.accept("d-up", self.setKey, ["back", 0])

        self.accept("e", self.setKey, ["right", 1])
        self.accept("e-up", self.setKey, ["right", 0])
        self.accept("s", self.setKey, ["right", 1])
        self.accept("s-up", self.setKey, ["right", 0])

        self.accept("wheel_up", self.setKey, ["wheel-in", 1])
        self.accept("wheel_down", self.setKey, ["wheel-out", 1])
        self.accept("page_up", self.setKey, ["zoom-in", 1])
        self.accept("page_up-up", self.setKey, ["zoom-in", 0])
        self.accept("page_down", self.setKey, ["zoom-out", 1])
        self.accept("page_down-up", self.setKey, ["zoom-out", 0])

    def setKey(self, key, value):
        if not self.isTyping:
            self.keyMap[key] = value

    def autoRun(self):
        if not self.keyMap["autoRun"]:
            self.setKey("autoRun", 1)
            self.setKey("forward", 1)
        else:
            self.setKey("autoRun", 0)
            self.setKey("forward", 0)


class chatRegulator(DirectObject):
    def __init__(self, clientClass, keysClass):
        self.maxMessages = 14
        self.messageList = []
        self.client = clientClass
        self.keys = keysClass
        # for gui debug
        self.accept("p", self.getWidgetTransformsF)
        # Create GUI
        # self.frame =
        self.chatInput = DirectEntry(initialText="Press 't' or click here to chat",
                                     cursorKeys=1,
                                     numLines=1,
                                     command=self.send,
                                     focusInCommand=self.handleTpress,
                                     focusOutCommand=self.resetText,
                                     focus=0,
                                     width=20)
        # self.chatInput.setPos(-1.31667,0,-0.97)
        self.chatInput.setScale(0.05)
        self.chatInput.reparentTo(base.a2dBottomLeft)
        self.chatInput.setPos(.05, 0, .05)

        self.messages = []
        self.txt = []
        for k in range(14):
            self.txt.append(OnscreenText(mayChange=1))
            self.messages.append(DirectLabel(activeState=1, text="hi"))
            # self.messages[k].setScale(0.0498732)
            # self.messages[k].setPos(-1.31667,0,-0.9)
        self.accept("t", self.handleTpress)
        self.accept("control-t", self.resetText)
        self.calls = 0

    def handleTpress(self):
        if not self.keys.isTyping:
            self.clearText()

    def clearText(self):
        self.chatInput.enterText('')
        self.keys.isTyping = True
        self.chatInput["focus"] = True

    def resetText(self):
        self.chatInput.enterText('')
        self.keys.isTyping = False

    # def leaveText(self):
    #  self.keys.isTyping = False
    def send(self, text):
        self.datagram = PyDatagram()
        self.datagram.addString("chat")
        self.datagram.addString(text)
        self.client.cWriter.send(self.datagram, self.client.Connection)

    def setText(self, text):
        self.index = 0
        # put the messages on screen
        self.messageList.append(text)
        if (len(self.messageList) > 14):
            self.messageList.reverse()
            del self.messageList[14]
            self.messageList.reverse()
        for k in self.messageList:
            self.text(k, (-.95, (-.8 + (.06 * self.index))), self.index)
            self.index += 1

    def getWidgetTransformsF(self):
        for child in aspect2d.getChildren():
            print child, "  position = ", child.getPos()
            print child, "  scale = ", child.getScale()

    def text(self, msg, position, index):
        self.txt[index].destroy()
        self.txt[index] = OnscreenText(text=msg, pos=position, fg=(1, 1, 1, 1), align=TextNode.ALeft, scale=.05,
                                       mayChange=1)
        self.txt[index].reparentTo(base.a2dBottomLeft)
        self.txt[index].setPos(.05, .15 + .05 * index)
