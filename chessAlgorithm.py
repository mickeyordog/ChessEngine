import pygame 
import pieces
import board

pygame.init() 
 
black = (0,0,0)
gray = (105,105,105) 
darkGray = (65,65,65) 
white = (255,255,255)
darkWhite = (125, 125, 125)
blue = (0, 0, 255)
yellow = (255,255,102)
darkYellow = (204,204,0)

squareSide = 60
gameWidth = squareSide * 8
gameHeight = squareSide * 8
# boardWidth = gameWidth * 3/4

display_surface = pygame.display.set_mode((gameWidth, gameHeight)) 
pygame.display.set_caption('Chess AI') 

manager = board.Manager()

board = manager.board
def displayBoard():
	for i in range(len(board)):
		for j in range(len(board[0])):
			#draw squares
			if (board[i][j].isAvailableMove):
				if (i + j) % 2 == 0:
					pygame.draw.rect(display_surface, yellow, (j * squareSide, i * squareSide, squareSide, squareSide))
				else: 
					pygame.draw.rect(display_surface, darkYellow, (j * squareSide, i * squareSide, squareSide, squareSide))
			else:
				if (i + j) % 2 == 0:
					pygame.draw.rect(display_surface, white, (j * squareSide, i * squareSide, squareSide, squareSide))
				else: 
					pygame.draw.rect(display_surface, gray, (j * squareSide, i * squareSide, squareSide, squareSide))
			#draw pieces
			if board[i][j].contents:
				display_surface.blit(board[i][j].contents.getImg(), (j * squareSide, i * squareSide)) 

display_surface.fill(blue) 
manager.setupBoard()
displayBoard()
# infinite loop 
while manager.isPlaying: 
	if (not manager.isPlayerTurn):
		# manager.randomMove()
		manager.makeAIMove()
		displayBoard()
		manager.isPlayerTurn = True
	# iterate over the list of Event objects 
	# that was returned by pygame.event.get() method. 
	for event in pygame.event.get() :
		# print(event)
		if event.type == pygame.QUIT : 
			# deactivates the pygame library 
			pygame.quit()
			# quit the program. 
			quit() 
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if (manager.isPlayerTurn):
				#returns true if player moved a piece
				if (manager.handleClick(pygame.mouse.get_pos())):
					manager.isPlayerTurn = False
				displayBoard()
		elif event.type == pygame.KEYDOWN:
			if event.key==pygame.K_UP:
				pass
   		# Draws the surface object to the screen. 
		pygame.display.update() 
			
# import numpy as np

# gameboard = np.array([['r','n','b','q','k','b','n','r'],
# 					  ['p','p','p','p','p','p','p','p'],
# 					  ['.','.','.','.','.','.','.','.'],
# 					  ['.','.','.','.','.','.','.','.'],
# 					  ['.','.','.','.','.','.','.','.'],
# 					  ['.','.','.','.','.','.','.','.'],
# 					  ['P','P','P','P','P','P','P','P'],
# 					  ['R','N','B','Q','K','B','N','R']])
# turn = 0 #0 for init, 1 for white, 2 for black

# def drawBoard(board):
# 	print(' +----------------+')
# 	for y in range(len(board)):
# 		print(f'{8-y}|', end='')
# 		for x in range(len(board[0])):
# 			print(f'{board[y][x]} ', end='')
# 		print('|')
# 	print(' +----------------+')
# 	print('  A B C D E F G H')

# drawBoard(gameboard)
