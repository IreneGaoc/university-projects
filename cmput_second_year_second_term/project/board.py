'''
Jessica Prieto and Irene Gao

##### THE IMPOSSIBLE TIC TAC TOE GAME! #####

the goal is to generate moves for the computer such that the
computer is undefeated: either it always wins, or the game
results in a draw

nodes: (for reference)
	 0 | 1 | 2 
	 3 | 4 | 5
	 6 | 7 | 8
'''

from tkinter import messagebox
import random

class Board:
	'''back-end of the program'''

	def __init__(self):
		'''initialicomes the board'''
		self.board = [" "]*9

	def __repr__(self):
		'''printing the "permanent board" on the terminal'''
		return "%s | %s | %s \n%s | %s | %s \n%s | %s | %s \n" % \
				(self.board[0], self.board[1], self.board[2], \
				self.board[3], self.board[4], self.board[5], \
				self.board[6], self.board[7], self.board[8])

	def check_win(self, curr_player):
		''' checks if the player won

		input arguments:
			- self - checks the board
			- curr_player - the player's character ('X' or 'O')
		returns True if that player won'''
		
		wins = (self.board[0] == curr_player and self.board[1] == curr_player and self.board[2] == curr_player) or \
				(self.board[3] == curr_player and self.board[4] == curr_player and self.board[5] == curr_player) or \
				(self.board[6] == curr_player and self.board[7] == curr_player and self.board[8] == curr_player) or \
				(self.board[0] == curr_player and self.board[3] == curr_player and self.board[6] == curr_player) or \
				(self.board[1] == curr_player and self.board[4] == curr_player and self.board[7] == curr_player) or \
				(self.board[2] == curr_player and self.board[5] == curr_player and self.board[8] == curr_player) or \
				(self.board[0] == curr_player and self.board[4] == curr_player and self.board[8] == curr_player) or \
				(self.board[2] == curr_player and self.board[4] == curr_player and self.board[6] == curr_player)
		return wins

	def check_draw(self, user, com):
		''' (called by the "temporary board")
		checks if it's a draw only on the case if the board is full
		and neither the player nor the computer won the game'''
		if (self.empty_moves() == []) and (self.check_win(user)== False) and (self.check_win(com) == False):
			#messagebox.showinfo("tic tac toe", "IT'S A DRAW!")
			return True
		else:
			return False

	def check_full_draw(self):
		''' (called by the "permanent board" 
		checks if it's a draw only on the case if the board is full
		and neither the player nor the computer won the game'''
		if self.empty_moves() == []:
			print("DRAW!")
			messagebox.showinfo("tic tac toe", "IT'S A DRAW!")
			return True
		else:
			return False

	def is_empty(self, idx):
		'''checks if a node is empty
		returns True if it's empty'''

		if self.board[idx] == " ":
			return True
		else:
			return False 

	def empty_moves(self):
		'''generates a list of all empty moves'''

		moves = []
		for i in range(9):
			if self.is_empty(i):
				moves.append(i)
		return moves

	def move(self, user, idx):
		''' places a move on the "permanent board"
		returns True if user wins, and False otherwise'''
		check_empty = self.is_empty(idx)
		if idx >=0 and idx < 9 and check_empty == True:
			self.board[idx] = user
		else:
			print("user: %s" % user)
			print(self)
			raise ValueError("Invalid move")

		print(self)

		if self.check_win(user) == True:
			messagebox.showinfo("tic tac toe", "%s WINS, Start New Game?" % user)
			print("%s WINS" % user)
			#self.clearBoard()
			return True

		else:
			return False

	def temp_move(self, user, idx):
		''' places a move on the "temporary board"
		returns True if user wins, and False otherwise'''
		check_empty = self.is_empty(idx)
		if idx >=0 and idx < 9 and check_empty == True:
			self.board[idx] = user

		win = self.check_win(user)
		#if win == True:
			#print("%s gen win.." % y)

	def copy_temp(self):
		'''makes a copy of the permanent board to a temporary board to be used to check
		the moves on each node'''
		b_buf = Board()
		for i in range(9):
			b_buf.board[i] = self.board[i]

		return b_buf

	def del_move(self, user, idx):
		'''removes a move on the node
		can only be called by the "temporary board" '''
		check_empty = self.is_empty(idx)
		if idx >=0 and idx <9 and check_empty == False:
			self.board[idx] = " "
		else:
			raise ValueError("Invalid delete")

	def clearBoard(self):
		'''Clears the board for a new game'''
		self.board = [" "]*9

	def minimax(self, node, player):
		'''MINIMAX ALGORITHM
		calculates the score generated each time through depth first search:
		if player wins : score = depth - 10
		if computer wins : score = 10 - depth

		IMPUT ARGS:
		board: the tictactoe board used
		node: the last node played by the other player
		player: the current player
		'''

		def getmaxscore(val):
			'''helper function for max_val'''
			#print(val)
			curr_max = -100
			best = 0

			if val == []:
				return (-1,-1)

			for succ in val: #(succ, score)
				curr_max = max(curr_max, succ[1])
				if curr_max == -100:
					raise ValueError("max error")
				if succ[1] == curr_max:
					best = succ

			return best

		def getminscore(val): #val = (succ, score)
			'''helper function foe min_val'''
			#print(val)
			curr_min = 100
			best = 0

			if val == []:
				return (-1,-1)

			for succ in val:
				curr_min = min(curr_min, succ[1])
				if curr_min == 100:
					raise ValueError("min error")
				if succ[1] == curr_min:
					best = succ

			return best


		def max_val(board, node, user, comp, score, depth):
			'''INPUT ARGUMENTS:
				- board: the temporary board used for genetating the next value
				- node, the last node generated,
				- user : the player's character ("X" or "O")
				- comp : the computer's character ("X" or "O")
				- score : the score passed, used for calculating the best move
				- depth : current depth passed : the number of generated moves from the current node 
							that was inputted in the minimax function'''

			#initialize the buffer board
			b_buf = Board()
			b_buf = board.copy_temp()
			m_buf = b_buf.empty_moves()

			all_val = [] #stores the scores for each of the empty node
			for succ in m_buf:
				#place a move on the buffer board
				b_buf.temp_move(comp, succ)

				#check if it wins
				if b_buf.check_win(comp): 
					score = 10-depth
					val = (succ, score)
					all_val.append(val)
					b_buf.del_move(comp,succ) #remove temporary move to check the next one

				elif b_buf.check_draw(user,comp):
					val = (succ, 0)
					all_val.append(val)
					b_buf.del_move(comp,succ) #remove temporary move to check the next one

				else:
					depth = depth + 1
					buf = min_val(b_buf, succ, user, comp, score, depth)
					val = (succ, buf[1]) #succ : the next node, buf[1] : max score generated by max_val
					all_val.append(val)
					b_buf.del_move(comp,succ) #remove temporary move to check the next one

			maxscore = getmaxscore(all_val)

			return maxscore

		def min_val(board, node, user, comp, score, depth):
			'''INPUT ARGUMENTS:
				- board: the temporary board used for genetating the next value
				- node, the last node generated,
				- user : the player's character ("X" or "O")
				- comp : the computer's character ("X" or "O")
				- score : the score passed, used for calculating the best move
				- depth : current depth passed : the number of generated moves from the current node 
							that was inputted in the minimax function'''

			#initialize buffer board for checking the moves
			b_buf = Board()
			b_buf = board.copy_temp()
			m_buf = b_buf.empty_moves()

			all_val = [] 
			for succ in m_buf:
				b_buf.temp_move(user, succ)
				if b_buf.check_win(user):
					score = depth - 10
					val = (succ, score)
					all_val.append(val)
					b_buf.del_move(user,succ)
				elif b_buf.check_draw(user,comp):					
					val =(succ, 0)
					all_val.append(val)
					b_buf.del_move(user,succ)
				else:
					depth = depth + 1
					buf = max_val(b_buf, succ, user, comp, score, depth) 
					val = (succ, buf[1]) #succ : the next node, buf[1] : max score generated by max_val
					all_val.append(val)

			minscore = getminscore(all_val)

			return minscore #tuple with minimum score : (next node, minimum score)

		if player == True:
			user = "X"
			comp = "O"
		else:
			user = "O"
			comp = "X"
			
		minimax_val = max_val(self, node, user, comp, 0, 0)

		return minimax_val[0]