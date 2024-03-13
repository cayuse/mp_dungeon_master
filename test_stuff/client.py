from direct.showbase.ShowBase import ShowBase
from direct.distributed.ClientRepository import ClientRepository

class Client(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Set up the client repository
        self.clientRepository = ClientRepository()

        # Connect to the server
        self.clientRepository.connect('127.0.0.1', 9099)

        # Create the ball
        self.ball = loader.loadModel("client/client/models/pc/male2.egg")
        self.ball.reparentTo(render)

        # Set up task to move the ball
        self.taskMgr.add(self.moveBallTask, "MoveBallTask")

    def moveBallTask(self, task):
        # Sample movement code (you can replace this with your desired logic)
        dt = globalClock.getDt()
        self.ball.setPos(self.ball.getPos() + (0.1 * dt, 0, 0))
        return task.cont

client = Client()
