class Move:
	def __init__(self, finalX, finalY, initX, initY):
		self.pos = (finalX, finalY)
		self.initPos = (initX, initY)
		self.pieceTaken = None
		self.valueChange = 0
	def toString(self):
		return self.initPos[0],'', self.initPos[1], 'to', self.pos[0], '',self.pos[1]

class Piece:

	def __init__(self, x, y, isLight):
		self.x = x
		self.y = y
		self.isLight = isLight
		#sets name as light or dark + name of class (e.g. queen, king)
		self.name = ("light " if isLight else "dark ") + self.__class__.__name__.lower()
		#number of times it has moved, used for pawns
		self.timesMoved = 0

	def setImg(self, img):
		self.img = img

	def getImg(self):
		return self.img

	def getPos(self):
		return self.x + '' + self.y

	def __str__(self):
		return self.name

	#for use by king
	def getSurroundingMoves(self, board):
		moves = []
		for i in range(-1, 2):
			for j in range(-1, 2):
				if self.x + j >= 0 and self.x + j <= 7 and self.y + i >= 0 and self.y + i <= 7:
					if (not board[self.y + i][self.x + j].contents) or board[self.y + i][self.x + j].contents.isLight != self.isLight: 
						moves.append(Move(self.x + j, self.y + i, self.x, self.y))
		return moves

	#for use by rook and queen
	def getHorizontalVerticalMoves(self, board):
		moves = []
		#check left
		for j in range(self.x - 1, -1, -1):
			if (board[self.y, j].contents):
				# print("checking: ", j, self.y)
				if (board[self.y, j].contents.isLight != self.isLight):
					moves.append(Move(j, self.y, self.x, self.y))
				break
			else:
				moves.append(Move(j, self.y, self.x, self.y))
		#check right
		for j in range(self.x + 1, 8):
			if (board[self.y, j].contents):
				if (board[self.y, j].contents.isLight != self.isLight):
					moves.append(Move(j, self.y, self.x, self.y))
				break
			else:
				moves.append(Move(j, self.y, self.x, self.y))
		#check up
		for i in range(self.y - 1, -1, -1):
			if (board[i][self.x].contents):
				# print("checking: ", j, self.y)
				if (board[i][self.x].contents.isLight != self.isLight):
					moves.append(Move(self.x, i, self.x, self.y))
				break
			else:
				moves.append(Move(self.x, i, self.x, self.y))
		#check down
		for i in range(self.y + 1, 8):
			if (board[i][self.x].contents):
				if (board[i][self.x].contents.isLight != self.isLight):
					moves.append(Move(self.x, i, self.x, self.y))
				break
			else:
				moves.append(Move(self.x, i, self.x, self.y))

		return moves

	#for use by bishop and queen
	def getDiagonalMoves(self, board):
		moves = []
		#bottom right
		for i in range(1, 8):
			if self.x + i <= 7 and self.y + i <= 7:
					if not board[self.y + i][self.x + i].contents:
						moves.append(Move(self.x + i, self.y + i, self.x, self.y))
					else:
						if board[self.y + i][self.x + i].contents.isLight != self.isLight:
							moves.append(Move(self.x + i, self.y + i, self.x, self.y))
						break
			else:
				break
		# bottom left
		for i in range(1, 8):
			if self.x - i >= 0 and self.y + i <= 7:
					if not board[self.y + i][self.x - i].contents:
						moves.append(Move(self.x - i, self.y + i, self.x, self.y))
					else:
						if board[self.y + i][self.x - i].contents.isLight != self.isLight:
							moves.append(Move(self.x - i, self.y + i, self.x, self.y))
						break
			else:
				break
		#top right
		for i in range(1, 8):
			if self.x + i <= 7 and self.y - i >= 0:
					if not board[self.y - i][self.x + i].contents:
						moves.append(Move(self.x + i, self.y - i, self.x, self.y))
					else:
						if board[self.y - i][self.x + i].contents.isLight != self.isLight:
							moves.append(Move(self.x + i, self.y - i, self.x, self.y))
						break
			else:
				break
		#top left
		for i in range(1, 8):
			if self.x - i >= 0 and self.y - i >= 0:
					if not board[self.y - i][self.x - i].contents:
						moves.append(Move(self.x - i, self.y - i, self.x, self.y))
					else:
						if board[self.y - i][self.x - i].contents.isLight != self.isLight:
							moves.append(Move(self.x - i, self.y - i, self.x, self.y))
						break
			else:
				break
		return moves

	#for use by knight
	def getKnightMoves(self, board):
		potentialMoves = [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
		moves = []
		for move in potentialMoves:
			if self.x + move[0] >= 0 and self.x + move[0] <= 7 and self.y + move[1] >= 0 and self.y + move[1] <= 7:
				if not board[self.y + move[1]][self.x + move[0]].contents or board[self.y + move[1]][self.x + move[0]].contents.isLight != self.isLight:
					moves.append(Move(self.x + move[0], self.y + move[1], self.x, self.y))
		return moves

	#for use by pawn
	def getPawnMoves(self, board):
		moves = []
		for i in range(1, 2 if self.timesMoved > 0 else 3):
			if (self.isLight and self.y - i >= 0) or (not self.isLight and self.y + i <= 7):
				if not board[self.y + (-i if self.isLight else i)][self.x].contents:
					moves.append(Move(self.x, self.y + (-i if self.isLight else i), self.x, self.y))
				else:
					break
			else:
				break
		#attacking
		multiply = -1 if self.isLight else 1 #controls whether attacking up or down (light or dark)
		#check left
		if self.x > 0 and board[self.y + multiply][self.x - 1].contents:
			if (board[self.y + multiply][self.x - 1].contents.isLight != self.isLight):
				moves.append(Move(self.x - 1, self.y + multiply, self.x, self.y))
		#check right
		if self.x < 7 and board[self.y + multiply][self.x + 1].contents:
			if (board[self.y + multiply][self.x + 1].contents.isLight != self.isLight):
				moves.append(Move(self.x + 1, self.y + multiply, self.x, self.y))

		return moves


class Queen(Piece):
	def __init__(self, x, y, isLight):
		super().__init__(x, y, isLight)

	def getMoves(self, board):
		moves = self.getHorizontalVerticalMoves(board)
		moves.extend(self.getDiagonalMoves(board))
		return moves

class King(Piece):
	def __init__(self, x, y, isLight):
		super().__init__(x, y, isLight)

	def getMoves(self, board):
		return self.getSurroundingMoves(board)

class Bishop(Piece):
	def __init__(self, x, y, isLight):
		super().__init__(x, y, isLight)
	def getMoves(self, board):
		return self.getDiagonalMoves(board)

class Pawn(Piece):
	def __init__(self, x, y, isLight):
		super().__init__(x, y, isLight)
	def getMoves(self, board):
		return self.getPawnMoves(board)

class Rook(Piece):
	def __init__(self, x, y, isLight):
		super().__init__(x, y, isLight)
	def getMoves(self, board):
		return self.getHorizontalVerticalMoves(board)

class Knight(Piece):
	def __init__(self, x, y, isLight):
		super().__init__(x, y, isLight)
	def getMoves(self, board):
		return self.getKnightMoves(board)
