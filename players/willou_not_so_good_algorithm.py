from random import *
import numpy as np


class model:

    def __init__(self, load_trained):
        self.name = "Le Willou But Worse"  # put your name here

        self.current_game = np.array([])

        self.empty_board = np.array([(0, 1), (0, 8), (1, 2), (1, 9), (2, 3), (2, 10), (3, 4), (3, 11), (4, 5), (4, 12), (5, 6), (5, 13), (6, 7), (6, 14), (7, 15), (8, 9), (8, 16), (9, 10), (9, 17), (10, 11), (10, 18), (11, 12), (11, 19), (12, 13), (12, 20), (13, 14), (13, 21), (14, 15), (14, 22), (15, 23), (16, 17), (16, 24), (17, 18), (17, 25), (18, 19), (18, 26), (19, 20), (19, 27), (20, 21), (20, 28), (21, 22), (21, 29), (22, 23), (22, 30), (23, 31), (24, 25), (24, 32), (25, 26), (25, 33), (26, 27), (26, 34), (27, 28), (27, 35), (28, 29), (28, 36), (29, 30), (29, 37), (30, 31), (30, 38), (31, 39), (32, 33), (32, 40), (33, 34), (33, 41), (34, 35), (34, 42), (35, 36), (35, 43), (36, 37), (36, 44), (37, 38), (37, 45), (38, 39), (38, 46), (39, 47), (40, 41), (40, 48), (41, 42), (41, 49), (42, 43), (42, 50), (43, 44), (43, 51), (44, 45), (44, 52), (45, 46), (45, 53), (46, 47), (46, 54), (47, 55), (48, 49), (48, 56), (49, 50), (49, 57), (50, 51), (50, 58), (51, 52), (51, 59), (52, 53), (52, 60), (53, 54), (53, 61), (54, 55), (54, 62), (55, 63), (56, 57), (57, 58), (58, 59), (59, 60), (60, 61), (61, 62), (62, 63)])

        self.current_board = np.ones(112)

        if load_trained:
            self.load()
        else: 
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
    def did_i_win(self, result):
        pass


    # def fill_current_board(self, available_cells, empty_board, current_board):
    #     for i in range(len(empty_board)):
    #         if np.all(np.isin(empty_board[i], available_cells)):
    #             current_board[i] = 0
    #         else:
    #             current_board[i] = 1
    #     pass


    def play(self, board, available_cells, is_first_player):
        state = np.array(board)
        possible_moves = np.array(available_cells)
        box_to_check = np.array([])
        counter = 0
        index_to_send = 0
        for i in range(len(state)):
            box_to_check = state[i]
            for j in range(len(possible_moves)):
                if np.all(np.isin(possible_moves[j], box_to_check)):
                    index_to_send = j
                    counter += 1
            if counter == 1:
                return available_cells[index_to_send]
        return choice(available_cells)

