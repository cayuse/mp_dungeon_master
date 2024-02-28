from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.distributed.PyDatagram import PyDatagram

class World(DirectObject):  # This class will control anything related to the virtual world
    def __init__(self):
        self.timeSinceLastUpdate = 0

    def UpdateWorld(self, meClass, clientClass):
        # get the time since the last framerate
        self.elapsed = globalClock.getDt()
        # add it to the time since we last set our position to where the server thinks we are
        # add the elapsed time to the time since the last update sent to the server
        self.timeSinceLastUpdate += self.elapsed
        if (self.timeSinceLastUpdate > 0.1):
            self.datagram = PyDatagram()
            self.datagram.addString("positions")
            self.datagram.addFloat64(meClass.model.getX())
            self.datagram.addFloat64(meClass.model.getY())
            self.datagram.addFloat64(meClass.model.getZ())
            self.datagram.addFloat64(meClass.model.getH())
            self.datagram.addFloat64(meClass.model.getP())
            self.datagram.addFloat64(meClass.model.getR())
            self.datagram.addBool(meClass.isMoving)
            try:
                clientClass.cWriter.send(self.datagram, clientClass.Connection)
            except:
                print("No connection to the server. You are in stand alone mode.")
                return Task.done
            self.timeSinceLastUpdate = 0
        return Task.cont

    def UpdateName(self, meClass, clientClass):
        print("update name entered")
        self.datagram = PyDatagram()
        self.datagram.addString("newname")
        self.datagram.addString(meClass.username)
        try:
            clientClass.cWriter.send(self.datagram, clientClass.Connection)
        except:
            print("No connection to the server. You are in stand alone mode.")
