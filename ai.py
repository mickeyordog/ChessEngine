import board
import numpy as np
import math
import copy

def minimaxAB(manager, depth, alpha, beta, isMaximizer):
	# global count #number of times run in one session
	#evaluate board
	value = manager.boardValue
	#gameIsOver() check if no moves remaining
	if manager.gameIsOver() or depth > 3:
		# count += 1
		return value
	if isMaximizer:
		possibleMoves= manager.getAllMoves(False)
		print('num moves: ', len(possibleMoves))
		maxEval = -math.inf
		for move in possibleMoves:
			manager.selectedTile = manager.board[move.initPos[1]][move.initPos[0]]
			# print('black selected tile:',move.initPos[0],move.initPos[1])
			manager.makeMove(move.pos[0],move.pos[1],False)
			eval = minimaxAB(manager, depth + 1, alpha, beta, False)
			manager.undoMove(False)
			if (eval > maxEval):
				maxEval = eval
				bestMove = move
			alpha = max(alpha, eval)
			if beta <= alpha:
				break
		if depth == 0:
			# for tile in manager.board[1]:
			# 	print(tile.contents)
			return bestMove
		return maxEval
	else:
		possibleMoves= manager.getAllMoves(True)
		minEval = math.inf
		for move in possibleMoves:
			manager.selectedTile = manager.board[move.initPos[1]][move.initPos[0]]
			# print('white selected tile:',move.initPos[0],move.initPos[1])
			manager.makeMove(move.pos[0],move.pos[1],True)
			eval = minimaxAB(manager, depth + 1, alpha, beta, True)
			manager.undoMove(True)
			minEval = min(eval, minEval)
			beta = min(eval, beta)
			if beta <= alpha:
				break
		return minEval