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

from board import Board
from tkinter import *
from tkinter import messagebox
import board
import tkinter
import random


root = Tk()
root.title("tic tac toe (AN IMPOSSIBLE GAME)")


''' INITIALIZE GLOBAL VARIABLES '''
player = True # 'X' if true, 'O' if false
check = False # to check if the player chooses to let the computer make the first move

b = Board()
var = IntVar()
strn = StringVar()
strn2 = StringVar()

strn.set("SELECT A PLAYER")
strn2.set("Choose who starts")

class Application(Frame):
	'''front-end of the program'''	
	def sel(self):
		''' helper function for the radio buttons '''
		global player
		global check

		label = Label(root)
		label2 = Label(root)

		if player == True:
			user = "X"
		else:
			user = "O"

		if var.get() == 1: #player "X" is selected
			player = True
			strn.set("Your player : X")

			self.X["state"] = "disabled"
			self.O["state"] = "disabled"
			self.initmove(check)

		elif var.get() == 2: #player "O" is selected
			player = False
			strn.set("Your player : O")

			self.X["state"] = "disabled"
			self.O["state"] = "disabled"
			self.initmove(check)

		if var.get() == 3: #player starts
			check = False
			strn2.set("You start")
			self.play["state"] = "disabled"
			self.comp["state"] = "disabled"
			self.initmove(check)

		elif (var.get() == 4): #computer starts
			check = True
			strn2.set("Computer starts")
			self.play["state"] = "disabled"
			self.comp["state"] = "disabled"
			self.initmove(check)

	def initmove(self, check):
		''' initialize the board'''
		if (self.play["state"] == "disabled") and (self.X["state"] == "disabled"):
			self.move0["state"] = "active"
			self.move1["state"] = "active"
			self.move2["state"] = "active"
			self.move3["state"] = "active"
			self.move4["state"] = "active"
			self.move5["state"] = "active"
			self.move6["state"] = "active"
			self.move7["state"] = "active"
			self.move8["state"] = "active"
		
			if check == True:
				self.comp_player(9)

	def makemove(self, button, node):
		'''moves for each button'''
		global player
		global b

		if player == True and button["text"] == "  ":
			user = "X"
		elif player == False and button["text"] == "  ":
			user = "O"
		else:
			raise ValueError("choose another button")

		button["text"] = user

		check = b.move(user, node)
		if (check == True) or (b.check_full_draw == True):
			print("g")
			self.newgame()
		else:
			self.comp_player(node)


	def comp_player(self, node):
		''' generates the move in the input node for the computer'''

		global player
		global b

		player = not player
		if player == True:
			user = 'X'
		else:
			user = 'O'

		check = False

		#node = 9 if the player asks the computer to do the first move
		if node == 9:
			#generate random move
			move = random.randrange(9)
		else:
			# CALL MINIMAX TO CALCULATE NEXT MOVE
			move = b.minimax(node, player)
		if move == 0:
			self.move0["text"] = user
			check = b.move(user, 0)
		elif move == 1:
			self.move1["text"] = user
			check = b.move(user, 1)
		elif move == 2:
			self.move2["text"] = user
			check = b.move(user, 2)
		elif move == 3:
			self.move3["text"] = user
			check = b.move(user, 3)
		elif move == 4:
			self.move4["text"] = user
			check = b.move(user, 4)
		elif move == 5:
			self.move5["text"] = user
			check = b.move(user, 5)
		elif move == 6:
			self.move6["text"] = user
			check = b.move(user, 6)
		elif move == 7:
			self.move7["text"] = user
			check = b.move(user, 7)
		elif move == 8:
			self.move8["text"] = user
			check = b.move(user, 8)

		if (check == True): #player wins
			self.newgame()

		elif (b.check_full_draw() == True):
			self.newgame()

		else:
			player = not player	

	def empty_board(self):
		''' clears the GUI '''
		global player 

		self.move0["text"] = "  "
		self.move1["text"] = "  "
		self.move2["text"] = "  "
		self.move3["text"] = "  "
		self.move4["text"] = "  "
		self.move5["text"] = "  "
		self.move6["text"] = "  "
		self.move7["text"] = "  "
		self.move8["text"] = "  "

		b.clearBoard()
		
	def newgame(self):
		''' starts a new game 
		also a helper function for the 'NEW GAME' button '''

		global player
		
		self.empty_board()
		self.move0["state"] = "disabled"
		self.move1["state"] = "disabled"
		self.move2["state"] = "disabled"
		self.move3["state"] = "disabled"
		self.move4["state"] = "disabled"
		self.move5["state"] = "disabled"
		self.move6["state"] = "disabled"
		self.move7["state"] = "disabled"
		self.move8["state"] = "disabled"
		strn.set("Setp 1: SELECT A PLAYER")
		strn2.set("Step 2: Choose who starts")
		self.X["state"] = "normal"
		self.O["state"] = "normal"
		self.play["state"] = "normal"
		self.comp["state"] = "normal"

	def createWidgets(self):
		'''GUI properties'''

		fnt = 'Arial 30 bold'
		pad = 30
		w = 5
		h = 3

		#initialize nodes on the board
		self.move0 = Button(self, text = "  ", height = h, width = w, font = fnt, \
			activebackground = 'black', activeforeground = 'green', state = "disabled")
		self.move1 = Button(self, text = "  ", height = h, width = w, font = fnt, \
			activebackground = 'black', activeforeground = 'green', state = "disabled")
		self.move2 = Button(self, text = "  ", height = h, width = w, font = fnt, \
			activebackground = 'black', activeforeground = 'green', state = "disabled")
		self.move3 = Button(self, text = "  ", height = h, width = w, font = fnt, \
			activebackground = 'black', activeforeground = 'green', state = "disabled")
		self.move4 = Button(self, text = "  ", height = h, width = w, font = fnt, \
			activebackground = 'black', activeforeground = 'green', state = "disabled")
		self.move5 = Button(self, text = "  ", height = h, width = w, font = fnt, \
			activebackground = 'black', activeforeground = 'green', state = "disabled")
		self.move6 = Button(self, text = "  ", height = h, width = w, font = fnt, \
			activebackground = 'black', activeforeground = 'green', state = "disabled")
		self.move7 = Button(self, text = "  ", height = h, width = w, font = fnt, \
			activebackground = 'black', activeforeground = 'green', state = "disabled")
		self.move8 = Button(self, text = "  ", height = h, width = w, font = fnt, \
			activebackground = 'black', activeforeground = 'green', state = "disabled")

		#for node 0
		self.move0["command"] = lambda: self.makemove(self.move0,0)
		self.move0.config(bg ='black', fg = 'green')
		self.move0.grid({"row" : 1, "column" : 0})

		#for node 1
		self.move1["command"] = lambda: self.makemove(self.move1,1)
		self.move1.config(bg ='black', fg = 'green')
		self.move1.grid({"row" : 1, "column" : 1})

		#for node 2
		self.move2["command"] = lambda: self.makemove(self.move2,2)
		self.move2.config(bg ='black', fg = 'green')
		self.move2.grid({"row" : 1, "column" : 2})

		#for node 3
		self.move3["command"] = lambda: self.makemove(self.move3,3)
		self.move3.config(bg ='black', fg = 'green')
		self.move3.grid({"row" : 2, "column" : 0})

		#for node 4
		self.move4["command"] = lambda: self.makemove(self.move4,4)
		self.move4.config(bg ='black', fg = 'green')
		self.move4.grid({"row" : 2, "column" : 1})

		#for node 5
		self.move5["command"] = lambda: self.makemove(self.move5,5)
		self.move5.config(bg ='black', fg = 'green')
		self.move5.grid({"row" : 2, "column" : 2})

		#for node 6
		self.move6["command"] = lambda: self.makemove(self.move6,6)
		self.move6.config(bg ='black', fg = 'green')
		self.move6.grid({"row" : 3, "column" : 0})

		#for node 7
		self.move7["command"] = lambda: self.makemove(self.move7,7)
		self.move7.config(bg ='black', fg = 'green')
		self.move7.grid({"row" : 3, "column" : 1})

		#for node 8
		self.move8["command"] = lambda: self.makemove(self.move8,8)
		self.move8.config(bg ='black', fg = 'green')
		self.move8.grid({"row" : 3, "column" : 2})

		#for the radio buttons (choosing a player)
		label_text = Label(root, textvariable = strn, relief=RAISED)
		label_text["relief"] = "flat"
		label_text["pady"] = 10
		label_text.pack()
		self.X = Radiobutton(root, text="X", variable=var, value=1,
                  command=self.sel)
		self.X.pack( anchor = CENTER )
		self.O = Radiobutton(root, text="O", variable=var, value=2,
                  command=self.sel)
		self.O.pack( anchor = CENTER )

		#for the radio buttons (choosing who starts first)
		label2_text = Label(root, textvariable = strn2, relief=RAISED)
		label2_text["relief"] = "flat"
		label2_text["pady"] = 10
		label2_text.pack()
		self.play = Radiobutton(root, text="I start", variable=var, value=3,
                  command=self.sel)
		self.play.pack( anchor = CENTER )
		self.comp = Radiobutton(root, text="Comp starts", variable=var, value=4,
                  command=self.sel)
		self.comp.pack( anchor = CENTER )

		#QUIT BUTTON
		self.QUIT = Button(self)
		self.QUIT["text"] = "QUIT"
		self.QUIT["fg"] = "red"
		self.QUIT["command"] = self.quit
		self.QUIT["width"] = 10
		self.QUIT.grid({"row" : 5, "column" : 0})

		#NEW GAME BUTTON
		self.NEWGAME = Button(self)
		self.NEWGAME["text"] = "New Game"
		self.NEWGAME["fg"] = "blue"
		self.NEWGAME["command"] = self.newgame
		self.NEWGAME["width"] = 10
		self.NEWGAME.grid({"row" : 5, "column" : 2})
		

	def __init__(self, master = None):
		label = Label(root)
		Frame.__init__(self, master)

		self.pack()
		self.createWidgets()


root.geometry("450x620")
app = Application(master=root)
app.mainloop()