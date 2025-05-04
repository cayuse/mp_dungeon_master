from panda3d.core import *
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
import re
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

class Server(QueuedConnectionManager):
	def __init__(self, port: int, backlog: int):
		super().__init__()
		self.cListener = QueuedConnectionListener(self, 0)
		self.cReader = QueuedConnectionReader(self, 0)
		self.cWriter = ConnectionWriter(self, 0)
		self.port = port
		self.backlog = backlog
		try:
			self.socket = self.openTCPServerRendezvous(self.port, self.backlog)
			self.cListener.addConnection(self.socket)
			print(f"Server started on port {self.port}")
		except Exception as e:
			print(f"Failed to start server: {e}")
			raise

	def tskReaderPolling(self, regClass: 'PlayerReg') -> Task:
		try:
			if self.cReader.dataAvailable():
				self.datagram = NetDatagram()
				if self.cReader.getData(self.datagram):
					regClass.updateData(self.datagram.getConnection(), self.datagram, self)
		except Exception as e:
			print(f"Error in reader polling: {e}")
		return Task.cont

	def tskListenerPolling(self, regClass: 'PlayerReg') -> Task:
		try:
			if self.cListener.newConnectionAvailable():
				self.rendezvous = PointerToConnection()
				self.netAddress = NetAddress()
				self.newConnection = PointerToConnection()
				if self.cListener.getNewConnection(self.rendezvous, self.netAddress, self.newConnection):
					self.newConnection = self.newConnection.p()
					regClass.PlayerList.append(player())
					regClass.PlayerList[regClass.active].connectionID = self.newConnection
					regClass.sendInitialInfo(regClass.active, self)
					regClass.active += 1
					self.cReader.addConnection(self.newConnection)
					print(f'New connection received from {self.netAddress}')
		except Exception as e:
			print(f"Error in listener polling: {e}")
		return Task.cont

	
# Constants
UPDATE_INTERVAL = 0.1  # seconds between position updates
MAX_PLAYERS = 100  # maximum number of players allowed

class PlayerReg(DirectObject): #This class will hold anything that is related to regulating clients
	def __init__(self):
		self.PlayerList: list[player] = []
		self.active: int = 0
		self.timeSinceLastUpdate: float = 0
		
	
	def updatePlayers(self, serverClass: Server, data: str, type: str) -> Task:
		if type == "positions":
			try:
				self.elapsed = globalClock.getDt()
				self.timeSinceLastUpdate += self.elapsed
				if self.timeSinceLastUpdate > UPDATE_INTERVAL:
					if self.active:
						self.datagram = PyDatagram()
						self.datagram.addString("update")
						self.datagram.addFloat64(self.active)
						for k in range(self.active):
							self.datagram.addFloat64(self.PlayerList[k].currentPos['x'])
							self.datagram.addFloat64(self.PlayerList[k].currentPos['y'])
							self.datagram.addFloat64(self.PlayerList[k].currentPos['z'])
							self.datagram.addFloat64(self.PlayerList[k].currentPos['h'])
							self.datagram.addFloat64(self.PlayerList[k].currentPos['p'])
							self.datagram.addFloat64(self.PlayerList[k].currentPos['r'])
							self.datagram.addBool(self.PlayerList[k].isMoving)
						for k in self.PlayerList:
							self.conn = k.connectionID
							serverClass.cWriter.send(self.datagram, self.conn)
					self.timeSinceLastUpdate = 0
			except Exception as e:
				print(f"Error updating player positions: {e}")
			return Task.cont
		
		if type == "chat":
			try:
				self.datagram = PyDatagram()
				self.datagram.addString("chat")
				self.text = data
				self.datagram.addString(self.text)
				print(f"Chat message: {self.text}")
				for k in self.PlayerList:
					serverClass.cWriter.send(self.datagram, k.connectionID)
			except Exception as e:
				print(f"Error sending chat message: {e}")

				
		
	def updateData(self, connection, datagram: NetDatagram, serverClass: Server) -> None:
		try:
			self.iterator = PyDatagramIterator(datagram)
			self.type = self.iterator.getString()
			if self.type == "positions":
				for k in self.PlayerList:
					if k.connectionID == connection:
						k.currentPos['x'] = self.iterator.getFloat64()
						k.currentPos['y'] = self.iterator.getFloat64()
						k.currentPos['z'] = self.iterator.getFloat64()
						k.currentPos['h'] = self.iterator.getFloat64()
						k.currentPos['p'] = self.iterator.getFloat64()
						k.currentPos['r'] = self.iterator.getFloat64()
						k.isMoving = self.iterator.getBool()

			elif self.type == "chat":
				msg = self.iterator.getString()
				self.chatHelper(connection, serverClass, msg)

			elif self.type == "newname":
				name = self.iterator.getString()
				print(f"New name received: {name}")
				for k in self.PlayerList:
					if k.connectionID == connection:
						k.username = name
		except Exception as e:
			print(f"Error updating data: {e}")

	def chatHelper(self, connection, serverClass: Server, msg: str) -> None:
		try:
			slash = re.compile('^/')
			if slash.match(msg):
				self.commandHelper(connection, serverClass, msg)
			else:
				for k in self.PlayerList:
					if k.connectionID == connection:
						msg = f"{k.username}: {msg}"
						self.updatePlayers(serverClass, msg, "chat")
		except Exception as e:
			print(f"Error in chat helper: {e}")

	def commandHelper(self, connection, serverClass: Server, msg: str) -> None:
		try:
			command = msg.split(' ', 1)[0]
			if command == "/username":
				for idx, k in enumerate(self.PlayerList):
					if k.connectionID == connection:
						name = k.username
						self.PlayerList[idx].username = msg.split(' ', 1)[1]
						msg = f"{name} is now known as {self.PlayerList[idx].username}"
						self.updatePlayers(serverClass, msg, "chat")
			elif command == "/quit":
				self.handlePlayerQuit(connection, serverClass)
		except Exception as e:
			print(f"Error in command helper: {e}")

	def handlePlayerQuit(self, connection, serverClass: Server) -> None:
		try:
			for idx, k in enumerate(self.PlayerList):
				if k.connectionID == connection:
					msg = f"{k.username} has left the game"
					self.updatePlayers(serverClass, msg, "chat")
					del self.PlayerList[idx]
					self.active -= 1
					break
		except Exception as e:
			print(f"Error handling player quit: {e}")

	def sendInitialInfo(self, i: int, server: Server) -> None:
		try:
			if i >= len(self.PlayerList):
				raise IndexError(f"Player index {i} out of range")
				
			self.con = self.PlayerList[i].connectionID
			self.datagram = PyDatagram()
			self.datagram.addString("init")
			self.datagram.addUint8(self.active)
			self.datagram.addFloat64(i)
			for k in self.PlayerList:
				self.datagram.addString(k.username)
				self.datagram.addFloat64(k.currentPos['x'])
				self.datagram.addFloat64(k.currentPos['y'])
				self.datagram.addFloat64(k.currentPos['z'])
			server.cWriter.send(self.datagram, self.con)
		except Exception as e:
			print(f"Error sending initial info: {e}")

class player(DirectObject):
	def __init__(self):
		super().__init__()
		self.connectionID: int = 0
		self.username: str = ""
		self.currentPos: dict[str, float] = {
			'x': 0.0,
			'y': 0.0,
			'z': 0.0,
			'h': 0.0,
			'p': 0.0,
			'r': 0.0
		}
		self.isMoving: bool = False

	def __str__(self) -> str:
		return f"Player(username='{self.username}', pos={self.currentPos}, moving={self.isMoving})"


		