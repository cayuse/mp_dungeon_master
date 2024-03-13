from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import Datagram

from direct.showbase.ShowBase import ShowBase
from direct.distributed.ServerRepository import ServerRepository

class MyServerObject(DistributedObject):
    def __init__(self, air):
        DistributedObject.__init__(self, air)

    def setBallPosition(self, x, y, z):
        self.sendUpdate('setBallPosition', [x, y, z])

class Server(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Set up the server repository
        self.serverRepository = ServerRepository(
            tcpPort=9099,
            allowAnonymousConnections=True
        )

        # Register the server object
        self.serverRepository.registerObjectClass(MyServerObject)

        # Start the server
        self.serverRepository.start()

        # Start the main loop
        self.run()

server = Server()
