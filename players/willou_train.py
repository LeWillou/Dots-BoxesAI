from random import *
import numpy as np
import csv


class model:

    def __init__(self, load_trained):
        self.name = "Le Willou"  # put your name here

        self.game_states = []

        self.game_choices = list()

        self.won_game_states = list()

        self.won_game_choices = list()

        self.empty_board = [(0, 1), (0, 8), (1, 2), (1, 9), (2, 3), (2, 10), (3, 4), (3, 11), (4, 5), (4, 12), (5, 6), (5, 13), (6, 7), (6, 14), (7, 15), (8, 9), (8, 16), (9, 10), (9, 17), (10, 11), (10, 18), (11, 12), (11, 19), (12, 13), (12, 20), (13, 14), (13, 21), (14, 15), (14, 22), (15, 23), (16, 17), (16, 24), (17, 18), (17, 25), (18, 19), (18, 26), (19, 20), (19, 27), (20, 21), (20, 28), (21, 22), (21, 29), (22, 23), (22, 30), (23, 31), (24, 25), (24, 32), (25, 26), (25, 33), (26, 27), (26, 34), (27, 28), (27, 35), (28, 29), (28, 36), (29, 30), (
            29, 37), (30, 31), (30, 38), (31, 39), (32, 33), (32, 40), (33, 34), (33, 41), (34, 35), (34, 42), (35, 36), (35, 43), (36, 37), (36, 44), (37, 38), (37, 45), (38, 39), (38, 46), (39, 47), (40, 41), (40, 48), (41, 42), (41, 49), (42, 43), (42, 50), (43, 44), (43, 51), (44, 45), (44, 52), (45, 46), (45, 53), (46, 47), (46, 54), (47, 55), (48, 49), (48, 56), (49, 50), (49, 57), (50, 51), (50, 58), (51, 52), (51, 59), (52, 53), (52, 60), (53, 54), (53, 61), (54, 55), (54, 62), (55, 63), (56, 57), (57, 58), (58, 59), (59, 60), (60, 61), (61, 62), (62, 63)]

        self.counter = 0

        self.dataset = list()

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
    def check_wins(self):
        return self.counter

    @staticmethod
    def did_i_win(self, result):
        
        if result == 1:
            self.counter += 1
            for i in range(len(self.game_states)):
                self.won_game_states.append(self.game_states[i])
        
            for i in range(len(self.game_choices)):
                self.won_game_choices.append(self.game_choices[i])
            self.game_choices.clear()
            self.game_states.clear()
        
        if self.counter == 10000:
            self.dataset.append(self.won_game_states)
            self.dataset.append(self.won_game_choices)
            dataset_to_save = np.array([self.dataset[0], self.dataset[1]])
            #print(dataset_to_save[1])
            # with open('dataset_training.csv', 'w') as csvfile:
            #     writer = csv.writer(csvfile, delimiter=',')
            #     writer.writerow(self.dataset)
            np.save('dataset_training.npy', dataset_to_save)
            
        pass

    def fill_current_board(self, available_cells, empty_board, current_board):
        for i in range(len(empty_board)):
            if empty_board[i] in available_cells:
                current_board[i] = 0
            else:
                current_board[i] = 1
        pass

    def play(self, board, available_cells, is_first_player):

        current_board = np.ones(112)

        self.fill_current_board(
            available_cells, self.empty_board, current_board)

        state = np.array(board)
        possible_moves = np.array(available_cells)
        box_to_check = np.array([])
        counter = 0
        index_to_send = -1
        k = 0
        cur_choice = np.zeros(112)

        self.game_states.append(current_board)
        #print(self.game_states)
        for i in range(len(state)):
            box_to_check = state[i]
            for j in range(len(possible_moves)):
                if np.all(np.isin(possible_moves[j], box_to_check)):
                    index_to_send = j
                    counter += 1
            
            if counter == 1:
                cur_choice[self.empty_board.index(available_cells[index_to_send])] = 1
                self.game_choices.append(cur_choice)
                return available_cells[index_to_send]

            elif counter == 2:
                rand_index = choice(
                    [k for i in range(len(available_cells)) if k != j])
                # self.game_choices.append(available_cells[rand_index])
                cur_choice[self.empty_board.index(available_cells[rand_index])] = 1
                self.game_choices.append(cur_choice)
                return available_cells[rand_index]

        cell_to_send = choice(available_cells)
        cur_choice[self.empty_board.index(cell_to_send)] = 1
        self.game_choices.append(cur_choice)
        return cell_to_send
