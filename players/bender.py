from random import *

class model:

	def __init__(self, load_trained):
		self.name = "FirstName LastName bender" # put your name here
		
		if load_trained:
			self.load()
		else :
			self.build()
	

	def build(self):
		print("create new model")
		pass
	

	def load(self):
		print("load existing model")
		pass


	def save(self):
		print("save good model")
		pass


	def play(self, board, available_cells, is_first_player):
		return choice(available_cells) # random available cell
