import math
import sys
import random
import numpy as np
import pygame

pink = (255, 80, 205)
black = (0, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
red = (0,0,255)

row_count = 6
column_count = 7

empty = 0

player = 0
AI = 1

player_piece = 1
AI_piece = 2

turn_detection = True

while turn_detection:
    turn = input("please who want star game:chose(AI  or  me):")
    try:
        if turn.lower() == "me":
            turn = player
            turn_detection = False
        elif turn.lower() == "ai" :
            turn = AI
            turn_detection = False
    except:
        pass




def create_board():
    board = np.zeros((row_count, column_count))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[row_count - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(row_count):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # check horizental location for win
    for i in range(row_count):
        for j in range(column_count - 3):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == piece:
                return True

    # check vertical  location for win
    for i in range(row_count - 3):
        for j in range(column_count):
            if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == piece:
                return True

    # check positively sloped diagnols
    for i in range(row_count - 3):
        for j in range(column_count - 3):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == piece:
                return True

    # check positively sloped diagnols
    for i in range(3, row_count):
        for j in range(column_count - 3):
            if board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == board[i - 3][j + 3] == piece:
                return True
def evaluate_window(window,piece):
    score = 0
    opp_piece = player_piece
    if piece == player_piece:
        opp_piece = AI_piece

    if window.count(piece) == 4:
        score += 100000
    elif window.count(piece) == 3 and window.count(empty) == 1:
        score += 150
    elif window.count(piece) == 2 and window.count(empty) == 2:
        score += 5


    if window.count(opp_piece) == 3 and window.count(empty) == 1:
        score -= 40

    return score




def score_position(board,piece):

     score = 0

     #score center column
     center_array = [int(i) for i in list(board[:,column_count//2])]
     center_count = center_array.count(piece)
     score += center_count*6
     #score horizontal
     for i in range(row_count):
         row_array = [int(r) for r in list(board[i,:])]
         for j in range(column_count-3):
             window = row_array[j:j+4]
             score += evaluate_window(window,piece)

     # score vertical
     for j in range(column_count):
         col_array = [int(c) for c in list(board[:,j])]
         for i in range(row_count-3):
             window = col_array[i:i+4]
             score += evaluate_window(window,piece)



#score positive diagonal
     for i in range(row_count - 3):
         for j in range(column_count - 3):
             window = [board[i+d][j+d] for d in range(4)]
             score += evaluate_window(window,piece)

#score negetive diagnal
     for i in range(3, row_count):
         for j in range(column_count - 3):
             window = [board[i-d][j+d] for d in range(4)]
             score += evaluate_window(window,piece)


     return score

def is_terminal_node(board):

       return winning_move(board,player_piece) or winning_move(board,AI_piece) or len(get_valid_locations(board)) == 0

def minimax(board,depth,alpha,beta,maximizingplayer):
    # opp_piece = player_piece
    # if piece == player_piece:
    #     opp_piece = AI_piece
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_piece):
                return (None,50000000)
            elif winning_move(board, player_piece):
                return (None,-50000000)
            else: # game is over ,no more valid move
                return (None,0)
        else: #depth is zero
            return (None,score_position(board,AI_piece))
    if maximizingplayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board,col)
            b_copy = board.copy()
            drop_piece(b_copy,row,col,AI_piece)
            new_score = minimax(b_copy,depth-1,alpha,beta,False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(value,alpha)
            if alpha >= beta:
                break
        return column,value

    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board,col)
            b_copy = board.copy()
            drop_piece(b_copy,row,col,player_piece)
            new_score = minimax(b_copy,depth-1,alpha,beta,True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value,beta)
            if alpha >= beta:
                break

        return column,value



def get_valid_locations(board):
    valid_locations = []
    for col in range(column_count):
        if is_valid_location(board,col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board,piece):
    valid_locations = get_valid_locations(board)
    best_score = -50
    best_column = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board,col)
        temp_board = board.copy()
        drop_piece(temp_board,row,col,piece)
        score = score_position(temp_board,piece)
        if score >  best_score:
            best_score = score
            best_column = col
    return best_column


def drow_board(board):
    for i in range(row_count):
        for j in range(column_count):
            pygame.draw.rect(screen, pink, (j * SQUARESIZE, i * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, black, (
            int(j * SQUARESIZE + SQUARESIZE / 2), int(i * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), radius)
    for i in range(row_count):
        for j in range(column_count):
            if board[i][j] == player_piece:
                pygame.draw.circle(screen, blue, (
                int(j * SQUARESIZE + SQUARESIZE / 2), height - int(i * SQUARESIZE + SQUARESIZE / 2)), radius)
            elif board[i][j] == AI_piece:
                pygame.draw.circle(screen, yellow, (
                int(j * SQUARESIZE + SQUARESIZE / 2), height - int(i * SQUARESIZE + SQUARESIZE / 2)), radius)

    pygame.display.update()


board = create_board()
print_board(board)
#turn = AI
game_over = False

pygame.init()

SQUARESIZE = 100

width = column_count * SQUARESIZE
height = (row_count + 1) * SQUARESIZE

size = (width, height)

radius = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
drow_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, SQUARESIZE))
            posy = event.pos[0]
            if turn == player:
                pygame.draw.circle(screen, blue, (posy, int(SQUARESIZE / 2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:

            pygame.draw.rect(screen, black, (0, 0, width, SQUARESIZE))
            # ask for player 1 input
            if turn == player:
                posy = event.pos[0]
                col = int(math.floor(posy / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, player_piece)
                else:
                    player_one = True
                    while player_one:
                        #print("please chose another column:")
                        #posy = event.pos[0]
                        #col = int(math.floor(posy / SQUARESIZE))
                        #if is_valid_location(board, col):
                        #    row = get_next_open_row(board, col)
                        #    drop_piece(board, row, col, player_piece)
                        #    player_one = False
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()

                            if event.type == pygame.MOUSEMOTION:
                                pygame.draw.rect(screen, black, (0, 0, width, SQUARESIZE))
                                posy = event.pos[0]
                                if turn == player:
                                    pygame.draw.circle(screen, blue, (posy, int(SQUARESIZE / 2)), radius)
                            pygame.display.update()

                            if event.type == pygame.MOUSEBUTTONDOWN:

                                pygame.draw.rect(screen, black, (0, 0, width, SQUARESIZE))
                                # ask for player 1 input
                                if turn == player:
                                    posy = event.pos[0]
                                    col = int(math.floor(posy / SQUARESIZE))

                                    if is_valid_location(board, col):
                                        row = get_next_open_row(board, col)
                                        drop_piece(board, row, col, player_piece)
                                        player_one = False

                if winning_move(board,player_piece):
                    lable = myfont.render("player 1 wins", 1, blue)
                    screen.blit(lable, (60, 10))
                    game_over = True
                turn += 1
                turn = turn % 2

                print_board(board)
                drow_board(board)




            # ask for player 2 input
    if turn == AI and not game_over :
        #col = random.randint(0,column_count-1)
        #col = pick_best_move(board,AI_piece)
        col, minimax_score = minimax(board,6,-math.inf,math.inf,True)


        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col,AI_piece)
        else:
            player_two = True
            while player_two:
                #print("please chose another column:")
                #col = random.randint(0,column_count-1)
                #col = pick_best_move(board, AI_piece)
                col, minimax_score = minimax(board, 7, -math.inf, math.inf, True)

                if is_valid_location(board, col):
                    pygame.time.wait(500)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_piece)
                    player_two = False
                else:
                    pass
                # for event in pygame.event.get():
                #
                #     if event.type == pygame.MOUSEMOTION:
                #         pygame.draw.rect(screen, black, (0, 0, width, SQUARESIZE))
                #         posy = event.pos[0]
                #     pygame.display.update()
                #
                #     if event.type == pygame.MOUSEBUTTONDOWN:
                #
                #         pygame.draw.rect(screen, black, (0, 0, width, SQUARESIZE))
                #         # ask for player 1 input
                #         if turn == AI and not game_over:
                #             #col = pick_best_move(board, AI_piece)
                #             col, minimax_score = minimax(board,7,-math.inf,math.inf,True)
                #
                #             if is_valid_location(board, col):
                #                 row = get_next_open_row(board, col)
                #                 drop_piece(board, row, col, AI_piece)
                #                 player_Two = False

        if winning_move(board, AI_piece):
            lable = myfont.render("AI wins", 1, yellow)
            screen.blit(lable, (60, 10))
            game_over = True

        print_board(board)
        drow_board(board)

        turn += 1
        turn = turn % 2

    if game_over:
        pygame.time.wait(3000)








