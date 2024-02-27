from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionNode, CollisionSphere, BitMask32
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Load the map
        self.map = self.loader.loadModel("map_model")
        self.map.reparentTo(self.render)

        # Create collision traverser
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        # Create collision node for the player
        self.playerNode = CollisionNode("player")
        self.playerNP = self.render.attachNewNode(self.playerNode)
        self.playerNode.addSolid(CollisionSphere(0, 0, 0, 1))

        # Attach the collision node to the player model
        self.player = Actor("player_model")
        self.player.reparentTo(self.render)
        self.player.setCollideMask(BitMask32.allOn())
        self.playerNP.reparentTo(self.player)

        # Add collision nodes to traverser
        self.cTrav.addCollider(self.playerNP, self.pusher)

        # Set up map boundaries
        self.mapBoundaries = self.render.attachNewNode(CollisionNode("mapBoundaries"))
        self.mapBoundaries.node().addSolid(CollisionSphere(0, 0, 0, 10))

        # Set up collision handling
        self.pusher.addCollider(self.playerNP, self.player, base.drive.node())
        self.accept("player-into-mapBoundaries", self.handleCollision)

    def handleCollision(self, entry):
        # Adjust player's position or velocity to prevent moving beyond map boundaries
        print("Collision detected!")

game = MyGame()
game.run()
