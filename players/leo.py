import copy
import random
import operator
from pprint import pprint

# Init your variables here

# Put your name Here
name = "Leo"

all_moves = []
for i in range(0, 8):
    for j in range(0, 8):
        if i <= 6 and j <= 6:
            all_moves.append((i * 8 + j, i * 8 + j + 1))
            all_moves.append((i * 8 + j, i * 8 + j + 8))
        elif j == 7:
            all_moves.append((i * 8 + j, i * 8 + j + 8))
        elif i == 7:
            all_moves.append((i * 8 + j, i * 8 + j + 1))

all_moves.pop(len(all_moves) - 1)


def nb_edge_in_box(available_cells, box):
    nb_edge = 0
    if (box[0], box[1]) not in available_cells:
        nb_edge += 1
    if (box[2], box[3]) not in available_cells:
        nb_edge += 1
    if (box[0], box[2]) not in available_cells:
        nb_edge += 1
    if (box[1], box[3]) not in available_cells:
        nb_edge += 1
    return nb_edge


def get_nb_boxes_max(board, available_cells, moves, move_id, last_box, last_move):
    available_cells.remove(last_move)
    board[board.index(last_box)][4] = 1

    for move in available_cells:
        for box in board:
            edges = [(box[0], box[1]), (box[2], box[3]), (box[0], box[2]), (box[1], box[3])]
            if move in edges and board[board.index(box)][4] == 0:
                nb_edges = nb_edge_in_box(available_cells, box)
                if nb_edges == 3:
                    moves[all_moves.index(move_id)] += 1
                    if box[0] == 27:
                        moves[all_moves.index(move_id)] += 6
                    elif box[0] in [9, 13, 37, 41]:
                        moves[all_moves.index(move_id)] += 2
                    get_nb_boxes_max(copy.deepcopy(board), copy.deepcopy(available_cells), moves, move_id, box, move)
            for k, v in moves.items():
                if v >= 32:
                    return


def get_best_move(board, available_cells, moves):
    for move in available_cells:
        for box in board:
            edges = [(box[0], box[1]), (box[2], box[3]), (box[0], box[2]), (box[1], box[3])]
            if move in edges and board[board.index(box)][4] == 0:
                nb_edges = nb_edge_in_box(available_cells, box)
                if nb_edges == 3:
                    moves[all_moves.index(move)] += 1
                    if box[0] == 27:
                        moves[all_moves.index(move)] += 6
                    elif box[0] in [9, 13, 37, 41]:
                        moves[all_moves.index(move)] += 2
                    get_nb_boxes_max(copy.deepcopy(board), copy.deepcopy(available_cells), moves, copy.deepcopy(move),
                                     copy.deepcopy(box), copy.deepcopy(move))
            for k, v in moves.items():
                if v >= 20:
                    return


def get_nb_boxes_min(board, available_cells, moves, move_id, last_move):
    available_cells.remove(last_move)
    for move in available_cells:
        for box in board:
            edges = [(box[0], box[1]), (box[2], box[3]), (box[0], box[2]), (box[1], box[3])]
            if move in edges and board[board.index(box)][4] == 0:
                nb_edges = nb_edge_in_box(available_cells, box)
                if nb_edges == 3:
                    moves[all_moves.index(move_id)] += 1
                    if box[0] == 27:
                        moves[all_moves.index(move_id)] += 6
                    elif box[0] in [9, 13, 37, 41]:
                        moves[all_moves.index(move_id)] += 2
                    get_nb_boxes_min(copy.deepcopy(board), copy.deepcopy(available_cells), moves, move_id, move)
            for k, v in moves.items():
                if v >= 20:
                    return


def get_worst_move(board, available_cells, moves):
    for move in available_cells:
        for box in board:
            edges = [(box[0], box[1]), (box[2], box[3]), (box[0], box[2]), (box[1], box[3])]
            if move in edges and board[board.index(box)][4] == 0:
                nb_edges = nb_edge_in_box(available_cells, box)
                if nb_edges == 2:
                    get_nb_boxes_min(copy.deepcopy(board), copy.deepcopy(available_cells), moves, copy.deepcopy(move),
                                     copy.deepcopy(move))
            for k, v in moves.items():
                if v >= 32:
                    return


def play(board, available_cells, player):
    best_moves = dict()
    for move in available_cells:
        best_moves[all_moves.index(move)] = 0
    get_best_move(copy.deepcopy(board), copy.deepcopy(available_cells), best_moves)

    if max(best_moves.items(), key=operator.itemgetter(1))[1] == 0:
        possible_move = dict()
        for move in available_cells:
            possible_move[all_moves.index(move)] = 0
        get_worst_move(copy.deepcopy(board), copy.deepcopy(available_cells), possible_move)
        min_value = min(possible_move.items(), key=operator.itemgetter(1))[1]
        min_keys = [k for k, v in possible_move.items() if v == min_value]
        return all_moves[random.choice(min_keys)]
        # return all_moves[min_keys[0]]

    max_value = max(best_moves.items(), key=operator.itemgetter(1))[1]
    max_keys = [k for k, v in best_moves.items() if v == max_value]
    return all_moves[random.choice(max_keys)]
    # return all_moves[max_keys[0]]
