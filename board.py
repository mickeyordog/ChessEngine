import pieces
import numpy as np
import pygame
import random
import ai
import math

class Tile():
	size = 60
	def __init__(self):
		# self.isOccupied = False
		self.isSelected = False
		self.isAvailableMove = False
		self.contents = None

class Manager():

	imgs = {
		'light queen': pygame.image.load('Assets/ql.png'),
		'dark queen': pygame.image.load('Assets/qd.png'),
		'light king': pygame.image.load('Assets/kl.png'),
		'dark king': pygame.image.load('Assets/kd.png'),
		'light bishop': pygame.image.load('Assets/bl.png'),
		'dark bishop': pygame.image.load('Assets/bd.png'),
		'light knight': pygame.image.load('Assets/nl.png'),
		'dark knight': pygame.image.load('Assets/nd.png'),
		'light pawn': pygame.image.load('Assets/pl.png'),
		'dark pawn': pygame.image.load('Assets/pd.png'),
		'light rook': pygame.image.load('Assets/rl.png'),
		'dark rook': pygame.image.load('Assets/rd.png'),
	}
	alphaToNum = {
		'A': 0,
		'B': 1,
		'C': 2,
		'D': 3,
		'E': 4,
		'F': 5,
		'G': 6,
		'H': 7
	}
	numToAlpha = {}
	values = {
		'Pawn': 10,
		'Knight': 30,
		'Bishop': 30,
		'Rook': 50,
		'Queen': 90,
		'King': 900
	}
	lightSquareTable = {
		'Pawn': [[0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,],
				[5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0,],
				[1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0,],
 				[0.5,  0.5, 1.0, 2.5, 2.5, 1.0,  0.5,  0.5,],
 				[0,  0,  0, 2.0, 2.0,  0,  0,  0,],
				[.5, -.5,-1.0,  0,  0,-1.0, -.5, .5,],
				[.5, 1.0, 1.0,-2.0,-2.0, 1.0, 1.0, .5,],
				[0,  0,  0,  0,  0,  0,  0,  0]]
	}
	darkSquareTable = {

	}

	def __init__(self, board = np.zeros((8,8), dtype=object), tilesWithLight = [], tilesWithDark = []):
		self.selectedTile = None #the tile that has been clicked
		self.highlightedTiles = []
		self.tilesWithLight = tilesWithLight #tiles containing light pieces
		self.tilesWithDark = tilesWithDark
		self.board = board
		self.isPlaying = True 
		self.isPlayerTurn = True
		#if empty board
		if (self.board[0][0] == 0):
			for i in range(len(self.board)):
				for j in range(len(self.board[0])):
					self.board[i][j] = Tile()
		else:
			pass
		random.seed(0)
		self.boardValue = 0
		# self.lastMove = None
		self.lastTakenPiece = None
		self.lastValueChange = 0
		self.movesMade = []

	def setupBoard(self):
		#dark pawns
		for x in range(8):
			self.addPiece(pieces.Pawn,x,1,False)
		#light pawns
		for x in range(8):
			self.addPiece(pieces.Pawn,x,6,True)
		#dark pieces
		self.addPiece(pieces.Rook,0,0,False)
		self.addPiece(pieces.Knight,1,0,False)
		self.addPiece(pieces.Bishop,2,0,False)
		self.addPiece(pieces.Queen,3,0,False)
		self.addPiece(pieces.King,4,0,False)
		self.addPiece(pieces.Bishop,5,0,False)
		self.addPiece(pieces.Knight,6,0,False)
		self.addPiece(pieces.Rook,7,0,False)
		

		self.addPiece(pieces.Rook,0,7,True)
		self.addPiece(pieces.Knight,1,7,True)
		self.addPiece(pieces.Bishop,2,7,True)
		self.addPiece(pieces.Queen,3,7,True)
		self.addPiece(pieces.King,4,7,True)
		self.addPiece(pieces.Bishop,5,7,True)
		self.addPiece(pieces.Knight,6,7,True)
		self.addPiece(pieces.Rook,7,7,True)
		
	#returns true if player made a move
	def handleClick(self, pos):
		#converts position to tile index
		x = int(pos[0]/Tile.size)
		y = int(pos[1]/Tile.size)
		newTile = self.board[y][x]

		if newTile.isAvailableMove:
			self.makeMove(x,y,True)
			return True
		else:
			#deselect old tiles
			for tile in self.highlightedTiles:
				tile.isAvailableMove = False
			if self.selectedTile and not self.selectedTile is newTile:
				self.selectedTile.isSelected = False

			if (newTile.contents and not newTile.contents.isLight):
				return False
			#select new tile
			if newTile.isSelected:
				self.selectedTile = None
				newTile.isSelected = False
			else:
				self.selectedTile = newTile
				newTile.isSelected = True
				self.highlightMoves(x, y)
			return False

	#must first set selected tile for initial tile
	def makeMove(self, x, y, isLight):
		newTile = self.board[y][x]

		print(self.selectedTile,x,y,isLight )
		self.movesMade.append(pieces.Move(x,y,self.selectedTile.contents.x,self.selectedTile.contents.y))

		
		# self.lastTakenPiece = None
		#if there is a piece to capture
		if (newTile.contents):
			#change last element of list
			self.movesMade[-1].pieceTaken = newTile.contents
			# self.lastTakenPiece = newTile.contents
			print('contents of new tile:',newTile.contents)
			#modify board's value
			if newTile.contents.isLight:
				value = self.values[newTile.contents.__class__.__name__]
				self.boardValue += value
				self.movesMade[-1].valueChange = value
			else:
				value = -self.values[newTile.contents.__class__.__name__]
				self.boardValue += value
				self.movesMade[-1].valueChange = value
			print('value:',self.boardValue)
			if (isLight):
				self.tilesWithDark.remove(newTile)
			else:
				self.tilesWithLight.remove(newTile)

		if (isLight):
			self.tilesWithLight.append(newTile)
			self.tilesWithLight.remove(self.selectedTile)
		else:
			self.tilesWithDark.append(newTile)
			self.tilesWithDark.remove(self.selectedTile)

		newTile.contents = self.selectedTile.contents
		newTile.contents.x = x
		newTile.contents.y = y
		newTile.contents.timesMoved += 1

		self.selectedTile.contents = None
		self.selectedTile = None
		#deselect old tile
		for tile in self.highlightedTiles:
			tile.isAvailableMove = False
			
	#isLight is the color of the player undoing the move
	def undoMove(self, isLight):
		print('num moves made:',len(self.movesMade))
		#removes last element of list
		lastMove = self.movesMade.pop()
		print('num moves made after pop:',len(self.movesMade))
		self.selectedTile = self.board[lastMove.pos[1]][lastMove.pos[0]]
		self.selectedTile.contents.timesMoved -= 2
		self.makeMove(lastMove.initPos[0], lastMove.initPos[1], isLight)
		#makeMove() adds undone move to this, so remove it (find a better way to do this, shouldn't add it in first place)
		self.movesMade.pop()
		if lastMove.pieceTaken:
			self.board[lastMove.pos[1]][lastMove.pos[0]].contents = lastMove.pieceTaken
			print('last taken piece:',lastMove.pieceTaken)
			# self.lastTakenPiece = None
			#append new piece to list!
			self.boardValue -= lastMove.valueChange
			print('value:',self.boardValue)
			if isLight:
				self.tilesWithDark.append(self.board[lastMove.pos[1]][lastMove.pos[0]])
			else:
				self.tilesWithLight.append(self.board[lastMove.pos[1]][lastMove.pos[0]])
		# self.boardValue -= self.lastValueChange
		# if isLight:
		# 	self.tilesWithDark.append(self.board[self.lastMove.pos[1]][self.lastMove.pos[0]])
		# else:
		# 	self.tilesWithLight.append(self.board[self.lastMove.pos[1]][self.lastMove.pos[0]])



	def addPiece(self, kind, x, y, isLight):
		self.board[y][x].contents = kind(x, y, isLight)
		self.board[y][x].contents.setImg(self.imgs[str(self.board[y][x].contents)])
		self.board[y][x].isOccupied = True
		if isLight:
			self.tilesWithLight.append(self.board[y][x])
		else:
			self.tilesWithDark.append(self.board[y][x])

	def highlightMoves(self, x, y):
		self.highlightedTiles.clear()
		if self.board[y][x].contents:
			moves = self.board[y][x].contents.getMoves(self.board)
			for move in moves:
				currentTile = self.board[move.pos[1]][move.pos[0]]
				currentTile.isAvailableMove = True
				self.highlightedTiles.append(currentTile)

	def getAllMoves(self, isLight):
		moves = []
		for tile in (self.tilesWithLight if isLight else self.tilesWithDark):
			moves.extend(tile.contents.getMoves(self.board))
		return moves

	def gameIsOver(self):
		return False

	def randomMove(self):
		randomTile = random.choice(self.tilesWithDark)
		# print(randomTile)
		piece = randomTile.contents
		possibleMoves = piece.getMoves(self.board)

		i = 0
		while (len(possibleMoves) == 0 and i < len(self.tilesWithDark)):
			randomTile = self.tilesWithDark[i]
			piece = randomTile.contents
			possibleMoves = piece.getMoves(self.board)
			i += 1
		#no available moves
		if (len(possibleMoves) == 0):
			return
		move = random.choice(possibleMoves).pos
		# destinationTile = self.board[move[1]][move[0]]
		# piece.hasMoved = True
		# piece.x = move[0]
		# piece.y = move[1]
		# destinationTile.contents = piece
		# randomTile.contents = None

		# self.tilesWithDark.remove(randomTile)
		# self.tilesWithDark.append(destinationTile)

		self.selectedTile = randomTile
		self.makeMove(move[0],move[1],False)

	def makeAIMove(self):
		move = ai.minimaxAB(self, 0, -math.inf, math.inf, True)
		self.selectedTile = self.board[move.initPos[1]][move.initPos[0]]
		self.makeMove(move.pos[0], move.pos[1], False)



	# def addQueen(self, x, y, isLight):
	# 	if isLight:
	# 		self.board[y][x] = pieces.Queen(x, y, isLight, pygame.image.load('Assets/ql.png'))
	# 	else:
	# 		self.board[y][x] = pieces.Queen(x, y, isLight, pygame.image.load('Assets/qd.png'))


