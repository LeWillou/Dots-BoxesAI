from random import *

class model:

	global q_table
	q_table = []
	global current_game
	current_game = []

	def __init__(self, load_trained):
		self.name = "willou" # put your name here

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

	@staticmethod
	def did_i_win(result):
		for i in range(len(current_game)):
			if result == 1:

				for l in range(len(q_table)):
					if q_table[l] in current_game:
						q_table[l][2] += 10
					else:
						current_game[i][2] += 10
						q_table.append(current_game[i])

			else:
				for l in range(len(q_table)):
					if q_table[l] in current_game:
						q_table[l][2] += 1
					else:
						current_game[i][2] += 10
						q_table.append(current_game[i])
				pass

	@staticmethod
	def get_q_table_length():
		for i in range(len(q_table)):
			return q_table[i][2]

	def play(self, board, available_cells, is_first_player):

		def clear_q_table(q_table):
			if len(q_table) >= 5000:
				for i in range(len(q_table)):
					print(q_table[i][2])

		def takeThird(array):
			return array[2]


		# print(available_cells)
		# print("\n\n")
		clear_q_table(q_table)

		current_choice = []
		make_a_choice = []
		is_found = 0

		for i in range(len(q_table)):
			if board in q_table[i]:
				is_found = 1

		# print("willou")
		# print(q_table)
		# print("\n\n\n")
		# print(board)

		if is_found == 0:
			current_choice.append(board)
			current_choice.append(choice(available_cells))
			current_choice.append(0)
			q_table.append(current_choice)
			#print(current_choice[1])
			return current_choice[1]


		else:
			for i in range(len(q_table)):
				if board in q_table[i]:
					make_a_choice.append(q_table[i])
			make_a_choice.sort(key=takeThird)
			current_choice = make_a_choice[0]
			current_game.append(current_choice)

			if not (current_choice[1] in available_cells):
				#print("Nope")
				current_choice.clear()
				current_choice.append(board)
				current_choice.append(choice(available_cells))
				current_choice.append(0)
				q_table.append(current_choice)
				#print(current_choice[1])
				return current_choice[1]

			else:
				#print(current_choice[1])
				return current_choice[1]
