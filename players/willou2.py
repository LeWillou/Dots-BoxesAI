from random import *

class model:

	# global q_table
	# q_table = []

	def __init__(self, load_trained):
		self.name = "willou2" # put your name here

		if load_trained:
			self.load()
		else :
			self.build()

		self.current_game = list()
		self.current_choice = list()
		self.q_table = list()


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
	def did_i_win(self, result):
		# if result == 1:
		# 	for i in range(len(current_game)):
		# 		if current_game[i] in q_table:
		# 			index_to_look_at = q_table.index(current_game[i])
		# 			q_table[index_to_look_at][2] += 10
		# 			current_game.clear()
		# 		else:
		# 			current_game[i][2] += 10
		# 			q_table.append(current_game[i])
		# 			current_game.clear()
		#
		# elif result == 0:
		# 	for i in range(len(current_game)):
		# 		if current_game[i] in q_table:
		# 			index_to_look_at = q_table.index(current_game[i])
		# 			q_table[index_to_look_at][2] += 1
		# 			current_game.clear()
		# 		else:
		# 			current_game[i][2] -= 1
		# 			q_table.append(current_game[i])
		# 			current_game.clear()
		#print(q_table[0])
		# if result == 0:
		# 	for i in range(len(self.current_game)):
		# 		if self.current_game[i] in q_table:
		# 			q_table.index(self.current_game[i])
		# 			self.current_game.clear()

		max_size = len(self.current_game) - 1

		if result == 1:
			for i in range(max_size):
				if self.current_game[i] in self.q_table:
					index_to_look_at = self.q_table.index(self.current_game[i])
					self.q_table[index_to_look_at][2] += 10
					print("True")
					pass

				else:
					self.current_game[i][2] += 10
					self.q_table.insert(0, self.current_game[i])
		else:
			for i in range(len(self.current_game)):
				if self.current_game[i] in self.q_table:
					index_to_look_at = self.q_table.index(self.current_game[i])
					self.q_table[index_to_look_at][2] += 1
					#print(self.q_table.index(self.current_game[i]))
					pass
				else:
					self.current_game[i][2] += 1
					self.q_table.insert(0,self.current_game[i])
					#print(self.current_game[i])

		self.current_game.clear()
		pass


	@staticmethod
	def get_q_table_length():
		for i in range(len(q_table)):
			return q_table[i][2]

	def play(self, board, available_cells, is_first_player):

		def clear_q_table(q_table):
			if len(q_table) >= 15000:
				for i in range(len(q_table)):
					print(q_table[i][2])

		def takeThird(array):
			return array[2]


		is_found = 0
		choice_list = list()
		state = [board, available_cells]

		if len(self.q_table) == 0:
			self.current_choice.append(state)
			cell_to_choose = choice(available_cells)
			self.current_choice.append(cell_to_choose)
			self.current_choice.append(0)
			self.current_game.insert(0, [[state], cell_to_choose, 0])
			#print(self.current_game)
			to_send = self.current_choice[1]
			self.current_choice.clear()
			return to_send

		else:
			for i in range(len(self.q_table)):
				if state in self.q_table[i]:
					choice_list.append(self.q_table[i])
					choice_list.sort(key=takeThird)
					is_found = 1

			#print(len(self.q_table))

			if is_found == 1:
				self.current_choice = choice_list[0]
				self.current_game.append(self.current_choice)
				to_send = self.current_choice[1]
				self.current_choice.clear()
				return to_send

			else:
				self.current_choice.append(state)
				cell_to_choose = choice(available_cells)
				self.current_choice.append(cell_to_choose)
				self.current_choice.append(0)
				self.current_game.insert(0, [[state], cell_to_choose, 0])
				#print(self.current_game)
				to_send = self.current_choice[1]
				self.current_choice.clear()
				return to_send
