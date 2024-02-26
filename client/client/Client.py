from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.gui.DirectGui import *
from direct.interval import ProjectileInterval
base.enableParticles()
from direct.particles.ParticleEffect import ParticleEffect
import sys

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

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
            print('connection failed')

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
