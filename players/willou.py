from random import *
import numpy as np
import _pickle as pickle

class model:

	# global q_table
	# q_table = []

	def __init__(self, load_trained):
		self.name = "willou" # put your name here

		if load_trained:
			self.load()
		else :
			self.build()

		self.current_game = list()
		self.q_table = np.zeros((12544, 113))

		self.epsilon = 0.3
		self.learning_rate = 0.2
		self.gamma = 0.85

		self.total_cells = [(0, 1), (0, 8), (1, 2), (1, 9), (2, 3), (2, 10), (3, 4), (3, 11), (4, 5), (4, 12), (5, 6), (5, 13), (6, 7), (6, 14), (7, 15), (8, 9), (8, 16), (9, 10), (9, 17), (10, 11), (10, 18), (11, 12), (11, 19), (12, 13), (12, 20), (13, 14), (13, 21), (14, 15), (14, 22), (15, 23), (16, 17), (16, 24), (17, 18), (17, 25), (18, 19), (18, 26), (19, 20), (19, 27), (20, 21), (20, 28), (21, 22), (21, 29), (22, 23), (22, 30), (23, 31), (24, 25), (24, 32), (25, 26), (25, 33), (26, 27), (26, 34), (27, 28), (27, 35), (28, 29), (28, 36), (29, 30), (29, 37), (30, 31), (30, 38), (31, 39), (32, 33), (32, 40), (33, 34), (33, 41), (34, 35), (34, 42), (35, 36), (35, 43), (36, 37), (36, 44), (37, 38), (37, 45), (38, 39), (38, 46), (39, 47), (40, 41), (40, 48), (41, 42), (41, 49), (42, 43), (42, 50), (43, 44), (43, 51), (44, 45), (44, 52), (45, 46), (45, 53), (46, 47), (46, 54), (47, 55), (48, 49), (48, 56), (49, 50), (49, 57), (50, 51), (50, 58), (51, 52), (51, 59), (52, 53), (52, 60), (53, 54), (53, 61), (54, 55), (54, 62), (55, 63), (56, 57), (57, 58), (58, 59), (59, 60), (60, 61), (61, 62), (62, 63)]


	def build(self):
		print("create new model")
		pass


	def load(self):
		print("load existing model")
		pass


	def save(self):
		print("save good model")
		pass


	# @staticmethod
	# def check_duplicates(self):
	# 	states_in_q_table = []
	# 	for i in range(len(self.q_table)):
	# 		states_in_q_table.insert(0, self.q_table[i][0])
	#
	# 	for states in states_in_q_table:
	# 		#print(states)
	# 		if states_in_q_table.count(states)>=400:
	# 			print("Duplicate found")
	# 			print("\n")
	# 	pass


	@staticmethod
	def did_i_win(self, result):
		if result == 1:
			for i in range(len(self.current_game) - 1):
				if np.all(np.isin(self.current_game[i][0], self.q_table)) == True:
					index_cell = np.where(self.total_cells == self.current_game[i][1])
					index_state = np.where(self.q_table == self.current_game[i][0])
					self.q_table[index_state[0][0], index_cell[0][1]-1] += self.learning_rate * (self.gamma * 1 - self.q_table[index_state[0][0], index_cell[0][1]-1])
				else:
					for l in range(len(self.q_table) - 1):
						if self.q_table[l, 0] == 0:
							self.q_table[l, 0] = self.current_game[i][0]
							index_cell = np.where(self.total_cells == self.current_game[i][1])
							self.q_table[l, index_cell[0][1]-1] += self.learning_rate * (self.gamma * 1 - self.q_table[index_state[0][0], index_cell[0][1]-1])
		else:
			for i in range(len(self.current_game) - 1):
				if np.all(np.isin(self.current_game[i][0], self.q_table)) == True:
					index_cell = np.where(self.total_cells == self.current_game[i][1])
					index_state = np.where(self.q_table == self.current_game[i][0])
					self.q_table[index_state[0][0], index_cell[0][1]-1] += self.learning_rate * (self.gamma * -1 - self.q_table[index_state[0][0], index_cell[0][1]-1])
				else:
					for l in range(len(self.q_table) - 1):
						if self.q_table[l, 0] == 0:
							self.q_table[l, 0] = self.current_game[i][0]
							index_cell = np.where(self.total_cells == self.current_game[i][1])
							self.q_table[l, index_cell[0][1]-1] += self.learning_rate * (self.gamma * -1 - self.q_table[index_state[0][0], index_cell[0][1]-1])
		pass


	@staticmethod
	def get_q_table_length():
		for i in range(len(q_table)):
			return q_table[i][2]

	def play(self, board, available_cells, is_first_player):
		is_found = 0

		max_reward = 0

		state = [board, available_cells[0:]]

		# print(len(self.total_cells))
		# print("\n\n")

		# if np.all(np.isin(state, self.q_table)) == True:
		# 	if choice(0,1) < self.epsilon:
		# 		#random
		# 		to_send = choice(available_cells)
		# 		current_choice = [state, to_send]
		# 		self.current_game.append(current_choice)
		# 		#print(to_send)
		# 		#print("Found in Q_Table")
		# 		return to_send
		#
		# 	else:
		# 		#exploit table
		# 		index = np.where(self.q_table == state)
		# 		max_reward = self.q_table[index[0][0], 1]
		# 		for i in range(len(self.total_cells) - 1):
		# 			if self.q_table[index[0][0], i+1] > max_reward:
		# 				max_reward = self.q_table[index[0][0], i+1]
		# 				max_reward_action = self.total_cells[i]
		#
		# 		to_send = max_reward_action
		# 		current_choice = [state, to_send]
		# 		self.current_game.append(current_choice)
		# 		#print(to_send)
		# 		#print("Found in Q_Table")
		# 		return to_send
		# else:
			#random
		to_send = choice(available_cells)
		current_choice = [state, to_send]
		self.current_game.append(current_choice)
		print(to_send)
		return to_send
