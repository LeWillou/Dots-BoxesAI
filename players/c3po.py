class model:

	def __init__(self, load_trained):
		self.name = "FirstName LastName c3po" # put your name here

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
		# print("c3po")
		# print(board)
		# print("\n\n\n")
		return available_cells[0] # first available cell
