from direct.distributed.ServerRepository import ServerRepository
from panda3d.core import ConfigVariableInt

class GameServerRepository(ServerRepository):
    def __init__(self):
        tcpPort = ConfigVariableInt('server-port', 9099).getValue()
        dcFileNames = ['direct.dc', 'yourOwnDCFile.dc']
        ServerRepository.__init__(self, tcpPort, dcFileNames=dcFileNames, threadedNet=True)

        ClientRepository.__init__(
            self,
            dcFileNames=dcFileNames,
            dcSuffix='AI',
            threadedNet=True)

    def deallocateChannel(self, doID):
        print("Client left us: ", doID)