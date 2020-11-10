# ----------------------------------------
#            Import librairies
# ----------------------------------------

import pygame
from importlib import import_module
import sys
import traceback
from collections import namedtuple
import time

# ----------------------------------------
#            Global variables to define
# ----------------------------------------

GRAPHIC_MODE = False

AI_PLAYER_1 = "players.willou_train"
AI_PLAYER_2 = "players.willou_not_so_good_algorithm"

LOAD_TRAINED_MODEL = True
NB_DUEL = 3000


# ----------------------------------------
#            Global fixed variables
# ----------------------------------------

BOARDSIZE = 8 #nb de points en ligne et colonne
BS = 80 #distance entre points

OWNER_NONE = 0
OWNER_AI1 = 1
OWNER_AI2 = 2

# the gameboard is stored as a list of points
# points contain their number, and the number of their connections
Point = namedtuple('Point', ['id', 'x', 'y', 'id_connected_points'])

init_board = []
board = [] #[id_point, coord x, coord y, id_connected_points]
boxes = [] #[id haut gauche, id haut droite, id bas gauche, id bas droite, possesseur]
moves_done = []
moves_remaining = []

score = [0, 0] # AI1, AI2
is_AI1_turn = True

# ----------------------------------------
#           Graphics functions
# ----------------------------------------

if GRAPHIC_MODE:
    from time import sleep
    from pygame import gfxdraw

    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 50)
    score_font = pygame.font.SysFont('Arial', 30)
    dot_font = pygame.font.SysFont('Arial', 15)

    #BS devrait être ici
    LINE_THICKNESS = 15 #epaisseur traits
    DOT_THICKNESS = 7
    size = BOARDSIZE * BS + BS #taille contenu fenêtre
    SURF = pygame.display.set_mode((size, size)) #surface fenêtre
    pygame.display.set_caption("Dots and  Boxes")

    BLACK = (0, 0, 0)
    RED = (255, 128, 0)
    BLUE = (0, 0, 255)

    moves_done_persons = []

    def disp_board():
        SURF.fill((255, 255, 255))

        # first lets draw the score at the top
        score_AI1 = score_font.render("{}: {}".format(ai_player_1.name , score[0]), True, BLUE)
        w, h = score_font.size("{}: {}".format(ai_player_1.name,score[0]))
        SURF.blit(score_AI1, (size // 2 - w - 10, 10))

        score_AI2 = score_font.render("{}: {}".format(ai_player_2.name, score[1]), True, RED)
        w2, h2 = score_font.size("{}: {}".format(ai_player_2.name, score[1]))
        SURF.blit(score_AI2, (size // 2 + 10, 10))

        # then, draw aeras
        for box in boxes:
            x1 = board[box[0]].x
            y1 = board[box[0]].y

            if box[4] == OWNER_AI1:
                pygame.draw.rect(SURF,(150,150,255),(x1,y1,BS,BS))
            elif box[4] == OWNER_AI2:
                pygame.draw.rect(SURF,(255,180,180),(x1,y1,BS,BS))

        # ahead, draw ticks with good color
        for i, move in enumerate(moves_done):
            point1 = board[move[0]] #position x, y et "partenaires" pour id A du déplacement i
            point2 = board[move[1]] #position x, y et "partenaires" pour id B du déplacement i

            pygame.draw.line(SURF, BLUE if moves_done_persons[i] else RED, (point1.x, point1.y), (point2.x, point2.y), LINE_THICKNESS)

        # on top, draw dots
        for i, point in enumerate(board):
            gfxdraw.filled_circle(SURF, point.x, point.y, DOT_THICKNESS, BLACK)

        #display '7' in the middle
        x1 = board[27].x
        y1 = board[27].y
        bonus = score_font.render("7".format(score[1]), True, (50,50,50))
        text_width, text_height = myfont.size("7")
        SURF.blit(bonus, (int(x1 + 50 - text_width / 2), int(y1 + 50 - text_height / 2)))

        #display '3' in the squares
        bonus = score_font.render("3".format(score[1]), True, (100,100,100))
        text_width, text_height = myfont.size("3")
        for i in [9, 13, 41, 45]:
            x1 = board[i].x
            y1 = board[i].y
            SURF.blit(bonus, (int(x1 + 50 - text_width / 2), int(y1 + 50 - text_height / 2)))

        pygame.display.update()

# ----------------------------------------
#           General functions
# ----------------------------------------

def timing(f): # permet de calculer temps d'exécution d'une fonction
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap

def init_game():
    global board
    global boxes

    board.clear()
    board = init_board.copy()

    boxes.clear()
    #[id haut gauche, id haut droite, id bas gauche, id bas droite, possesseur] donc ne peut pas faire range 0,55
    boxes.extend([[i, i+1, i+BOARDSIZE, i+1+BOARDSIZE, OWNER_NONE] for i in range(0,7)])
    boxes.extend([[i, i+1, i+BOARDSIZE, i+1+BOARDSIZE, OWNER_NONE] for i in range(8,15)])
    boxes.extend([[i, i+1, i+BOARDSIZE, i+1+BOARDSIZE, OWNER_NONE] for i in range(16,23)])
    boxes.extend([[i, i+1, i+BOARDSIZE, i+1+BOARDSIZE, OWNER_NONE] for i in range(24,31)])
    boxes.extend([[i, i+1, i+BOARDSIZE, i+1+BOARDSIZE, OWNER_NONE] for i in range(32,39)])
    boxes.extend([[i, i+1, i+BOARDSIZE, i+1+BOARDSIZE, OWNER_NONE] for i in range(40,47)])
    boxes.extend([[i, i+1, i+BOARDSIZE, i+1+BOARDSIZE, OWNER_NONE] for i in range(48,55)])


    moves_done.clear()
    moves_remaining.clear()
    for a in range(len(board)):
        for b in range(a, len(board)):
            if b == a:
                continue
            if not is_valid(a, b):
                continue
            moves_remaining.append((a, b))
    if GRAPHIC_MODE:
        moves_done_persons.clear()

    score[0] = 0
    score[1] = 0

def is_set_connected(point1, point2): #identifiants
    return True if (point1, point2) in moves_done or (point2, point1) in moves_done else False

def is_valid(point1, point2): #identifiants
    if is_set_connected(point1, point2):
        return False

    coord_p1 = board[point1]
    coord_p2 = board[point2]
    if coord_p1.y == coord_p2.y and (coord_p1.x == coord_p2.x + BS or coord_p1.x == coord_p2.x - BS): #coordonnées
        return True
    elif coord_p1.x == coord_p2.x and (coord_p1.y == coord_p2.y + BS or coord_p1.y == coord_p2.y - BS): #coordonnées
        return True
    else:
        return False

def is_move_closing_box(is_AI1, point1, point2):
    is_box = False

    for box in [item for item in boxes if (point1 in item and point2 in item)]:
        i = boxes.index(box)

        tmp = list(box) #necessaire pour ne pas detruire boxes
        tmp.remove(point1)
        tmp.remove(point2)

        if is_set_connected(tmp[0],tmp[1]) and ((is_set_connected(point1, tmp[0]) and is_set_connected(point2, tmp[1])) or (is_set_connected(point1, tmp[1]) and is_set_connected(point2, tmp[0]))):
            is_box = True #return pas car peut fermer plusieurs boites
            bonus = 1

            if i == 27: # id square bonus 7
                bonus = 7
            elif i in [9, 13, 41, 45]: # id squares bonus 7
                bonus = 3

            #applique gain
            if is_AI1:
                score[0] += bonus
                boxes[i][4] = OWNER_AI1
            else:
                score[1] += bonus
                boxes[i][4] = OWNER_AI2

    return is_box


def move(is_AI1, point1, point2):
    board[point1].id_connected_points.append(point2)
    board[point2].id_connected_points.append(point1)
    moves_done.append((point1, point2))
    return is_move_closing_box(is_AI1, point1, point2)

def move_graphic(is_AI1, point1, point2):
    board[point1].id_connected_points.append(point2)
    board[point2].id_connected_points.append(point1)
    moves_done.append((point1, point2))
    moves_done_persons.append(is_AI1)
    return is_move_closing_box(is_AI1, point1, point2)

def decide_and_move(ai_player, is_first_player):
    ai_choice = ai_player.play(boxes, moves_remaining, is_first_player)
    id_pt1 = ai_choice[0]
    id_pt2 = ai_choice[1]

    #verify that move is correct
    if (id_pt1,id_pt2) in moves_remaining:
        moves_remaining.remove((id_pt1,id_pt2))
    elif (id_pt2,id_pt1) in moves_remaining:
        moves_remaining.remove((id_pt2,id_pt1))
    else:
        raise NameError('invalid move')

    #if close a square, play again
    if move(is_first_player, id_pt1, id_pt2): #si ferme un carré, rejoue
        if len(moves_remaining) != 0: #fin de jeu
            decide_and_move(ai_player, is_first_player)
        else:
            return True

    #if it remains moves...
    return len(moves_remaining) == 0

def decide_and_move_graphic(ai_player, is_first_player):
    ai_choice = ai_player.play(boxes, moves_remaining, is_first_player)
    id_pt1 = ai_choice[0]
    id_pt2 = ai_choice[1]

    #verify that move is correct
    if (id_pt1,id_pt2) in moves_remaining:
        moves_remaining.remove((id_pt1,id_pt2))
    elif (id_pt2,id_pt1) in moves_remaining:
        moves_remaining.remove((id_pt2,id_pt1))
    else:
        raise NameError('invalid move')

    sleep(0.02)

    #if close a square, play again
    if move_graphic(is_first_player, id_pt1, id_pt2): #si ferme un carré, rejoue
        disp_board()
        if len(moves_remaining) != 0: #fin de jeu
            decide_and_move_graphic(ai_player, is_first_player)
        else:
            return True

    #if it remains moves...
    return len(moves_remaining) == 0

#@timing #décommenter pour voir temps d'exécution
def duel(current_duel, player1, player2):
    global is_AI1_turn
    ended = False

    print(f"\nDuel {current_duel} : {player1.name} vs {player2.name}")

    init_game()

    while not ended:
        is_AI1_turn = True #juste pour disqualification
        ended = decide_and_move(player1, True)

        if not ended:
            is_AI1_turn = False #juste pour disqualification
            ended = decide_and_move(player2, False)

    # game is finished!
    if score[0] > score[1]:
        print(f"{player1.name} won! Score: {score[0]} to {score[1]}")
        player1.did_i_win(player1, 1)


    else: #pas de nombre pair de points
        print(f"{player2.name} won! Score: {score[0]} to {score[1]}")
        player1.did_i_win(player1, 0)


def duel_graphic(current_duel, player1, player2):
    global is_AI1_turn
    ended = False

    print(f"\nDuel {current_duel} : {player1.name} vs {player2.name}")

    init_game()

    while not ended:
        for event in pygame.event.get(): #change to try except if possible
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        disp_board()
        is_AI1_turn = True
        ended = decide_and_move_graphic(player1, is_AI1_turn)

        if not ended:
            disp_board()
            is_AI1_turn = False
            ended = decide_and_move_graphic(player2, is_AI1_turn)

    # game is finished!
    disp_board()
    if score[0] > score[1]:
        print(f"{player1.name} won! Score: {score[0]} to {score[1]}")
        player1.did_i_win(player1, 1)
    else: #pas de nombre pair de points
        print(f"{player2.name} won! Score: {score[0]} to {score[1]}")
        player1.did_i_win(player1, 0)
    sleep(0.5)


# ----------------------------------------
#               Main entry
# ----------------------------------------

if __name__ == "__main__":
    global ai_player_1
    global ai_player_2

    counter = 0

    ai_player_1 = import_module(AI_PLAYER_1).model(load_trained=LOAD_TRAINED_MODEL) #instantiate class by loading or creating model
    ai_player_2 = import_module(AI_PLAYER_2).model(load_trained=LOAD_TRAINED_MODEL)

    pygame.init()

    #prepare init_board one time only
    for i in range(BOARDSIZE):
        for i2 in range(BOARDSIZE):
            init_board.append( Point(BOARDSIZE * i + i2, i2 * BS + BS, i * BS + BS, []))

    if not GRAPHIC_MODE:
        for i in range(NB_DUEL):
            try:
                duel(i, ai_player_1, ai_player_2)
            except Exception as inst:
                traceback.print_exc(file=sys.stdout)
                print(f"{ai_player_1.name if is_AI1_turn else ai_player_2.name} disqualified")
        #ai_player_1.check_duplicates(ai_player_1)

    else:
        for i in range(NB_DUEL):
            try:
                duel_graphic(i, ai_player_1, ai_player_2)
            except Exception as inst:
                print(inst)
                print(f"{ai_player_1.name if is_AI1_turn else ai_player_2.name} disqualified")

    if not LOAD_TRAINED_MODEL: #if training : save model file
        ai_player_1.save()
        ai_player_2.save()
