from ..myPan.myPan import base
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from ..Character import Character
import pickle
from panda3d.core import LPoint3f, LVecBase3f, NetDatagram
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class playerPacket:
    type: str = "None"
    message: str = "None"
    playerNum: int = 0
    Pos: LPoint3f = field(default_factory=lambda: LPoint3f(0, 0, 0))
    Hpr: LVecBase3f = field(default_factory=lambda: LVecBase3f(0, 0, 0))
    playerName: Optional[str] = None
    characterType: Optional[str] = None


class PlayerReg(DirectObject):  # This class will regulate the players
    def __init__(self):
        super().__init__()
        self.playerList: dict[int, Character] = {}
        self.numofplayers: int = 0
        self.enemy1: list = []
        self.numofenemy1: int = 0

    def tskProcessData(self, datagram: NetDatagram, me: Character, chatClass) -> Task:
        try:
            iterator = PyDatagramIterator(datagram)
            type = iterator.getString()
            if type == "None":
                return Task.cont
            if type == "init":
                # Process init packet
                playerNum = iterator.getUint8()
                numPlayers = iterator.getFloat64()
                for _ in range(int(numPlayers)):
                    username = iterator.getString()
                    x = iterator.getFloat64()
                    y = iterator.getFloat64()
                    z = iterator.getFloat64()
                    # Create or update player
                    if playerNum not in self.playerList:
                        self.playerList[playerNum] = Character()
                    player = self.playerList[playerNum]
                    player.username = username
                    player.setPos(LPoint3f(x, y, z))
                    player.getRoot().reparentTo(base.render)
            elif type == "update":
                # Process update packet
                numPlayers = iterator.getFloat64()
                for playerNum in range(int(numPlayers)):
                    x = iterator.getFloat64()
                    y = iterator.getFloat64()
                    z = iterator.getFloat64()
                    h = iterator.getFloat64()
                    p = iterator.getFloat64()
                    r = iterator.getFloat64()
                    isMoving = iterator.getBool()
                    # Update player position and state
                    if playerNum in self.playerList:
                        player = self.playerList[playerNum]
                        player.setPos(LPoint3f(x, y, z))
                        player.setHpr(LVecBase3f(h, p, r))
                        player.isMoving = isMoving
            elif type == "chat":
                # Process chat message
                message = iterator.getString()
                if chatClass:
                    chatClass.setText(message)
        except Exception as e:
            print(f"Error processing data: {e}")
        return Task.cont

    def processInit(self, packet: playerPacket) -> None:
        try:
            print("Initializing player")
            plr = packet.playerNum
            if plr in self.playerList:
                thisPlayer = self.playerList[plr]
            else:
                thisPlayer = Character()
                self.playerList[plr] = thisPlayer
            thisPlayer.setCharacter(packet.characterType)
            thisPlayer.setPlayerNum(packet.playerNum)
            thisPlayer.getRoot().reparentTo(base.render)
        except Exception as e:
            print(f"Error initializing player: {e}")

    def processUpdate(self, packet: playerPacket) -> None:
        try:
            plr = packet.playerNum
            if plr not in self.playerList:
                print(f"Warning: Received update for unknown player {plr}")
                return
            thisPlayer = self.playerList[plr]
            thisPlayer.setPos(packet.Pos)
            thisPlayer.setHpr(packet.Hpr)
        except Exception as e:
            print(f"Error processing update: {e}")

    def processChat(self, packet: playerPacket) -> None:
        try:
            text = packet.message
            # TODO: Implement chat display
            print(f"Chat message: {text}")
        except Exception as e:
            print(f"Error processing chat: {e}")

    def tskUpdateWorld(self, me: Character) -> Task:
        try:
            packet = playerPacket()
            packet.Pos = me.getPos()
            packet.Hpr = me.getHpr()
            serialized_data = pickle.dumps(packet)
            try:
                clientClass.cWriter.send(serialized_data)
            except Exception as e:
                print(f"No connection to the server. You are in stand alone mode: {e}")
                return Task.done
        except Exception as e:
            print(f"Error updating world: {e}")
        return Task.cont

    def UpdateName(self, meClass: Character, clientClass) -> None:
        try:
            print("Updating name")
            self.datagram = PyDatagram()
            self.datagram.addString("newname")
            self.datagram.addString(meClass.username)
            try:
                clientClass.cWriter.send(self.datagram, clientClass.Connection)
            except Exception as e:
                print(f"No connection to the server. You are in stand alone mode: {e}")
        except Exception as e:
            print(f"Error updating name: {e}")

    def updatePlayers(self, me: Character) -> Task:
        """Update the positions and states of all players in the game world."""
        try:
            # Update the number of players
            self.numofplayers = len(self.playerList)
            
            # Update each player's position and state
            for player_id, player in self.playerList.items():
                if player_id != me.playernum:  # Don't update our own position
                    # Update player position and rotation
                    root = player.getRoot()
                    root.setPos(root.getPos())
                    root.setHpr(root.getHpr())
                    
                    # Update animation state if needed
                    if hasattr(player, 'model') and player.model is not None:
                        if hasattr(player, 'isMoving') and player.isMoving:
                            if not player.model.getCurrentAnim() == "walk":
                                player.walk()
                        else:
                            if player.model.getCurrentAnim() == "walk":
                                player.stop()
            
            return Task.cont
        except Exception as e:
            print(f"Error updating players: {e}")
            return Task.cont
