import numpy as np
import matplotlib.pyplot as plt
import random as rd
import time

NUMBER_OF_MOVES = 4
SAMPLE_COUNT = 50




TIME_ONE_MOVE = 0.2

# 0 : purRandom
# 1 : monteCarloSearch
# 2 : greedySearch
# 3 : treeSearch
# 4 : UCS
USED_METHOD = 3


# used in treeSearch and UCS
GLOBAL_LENGTH = int(4 + np.log10(TIME_ONE_MOVE))




from game_functions import initialize_game, random_move, random_move_up_left, \
                            move_down, move_left,\
                            move_right, move_up,\
                            check_for_win, add_new_tile



def purRandom(board_with_first_move):
    nb_w = 0
    time0 = time.time()
    tot_score = 0
    while time.time()-time0<TIME_ONE_MOVE/NUMBER_OF_MOVES:
        nb_w +=1
        search_board = np.copy(board_with_first_move)
        search_board = add_new_tile(search_board)
        game_valid = True
        while game_valid:
            search_board, game_valid, score = random_move(search_board)
            if game_valid:
                search_board = add_new_tile(search_board)
                tot_score += score
    return tot_score/nb_w


def monteCarloSearch(board_with_first_move):
    time0 = time.time()
    max_score = 0
    while time.time()-time0<TIME_ONE_MOVE/NUMBER_OF_MOVES:
        tot_score = 0
        search_board = np.copy(board_with_first_move)
        search_board = add_new_tile(search_board)
        game_valid = True
        while game_valid:
            search_board, game_valid, score = random_move(search_board)
            if game_valid:
                search_board = add_new_tile(search_board)
                tot_score += score
        max_score = max(max_score, tot_score)
    return max_score


def greedySearch(board_with_first_move):
    tot_score = 0
    nb_w = 0
    time0 = time.time()
    while time.time()-time0<TIME_ONE_MOVE/NUMBER_OF_MOVES:
        nb_w += 1
        search_board = np.copy(board_with_first_move)
        search_board = add_new_tile(search_board)
        game_valid = True
        while game_valid:
            score_max = 0
            l = [move_left, move_up, move_down, move_right]
            l2 = []
            for i in range (len(l)):
                search_board, game_valid, score = l[i](search_board)
                if score > score_max and game_valid:
                    l2 = [(search_board, game_valid, score)]
                    score_max = score
                elif score == score_max and game_valid:
                    l2.append((search_board, game_valid, score))
            if len(l2)>0:
                search_board, game_valid, score = rd.choice(l2)
                search_board = add_new_tile(search_board)
                tot_score += score
    return tot_score/nb_w


def treeSearch(board_with_first_move):
    nb_w = 0
    tot_score = 0
    time0 = time.time()
    while time.time()-time0<TIME_ONE_MOVE/NUMBER_OF_MOVES:
        nb_w +=1
        search_board = np.copy(board_with_first_move)
        search_board = add_new_tile(search_board)
        game_valid = True
        nb_movement = 0
        while game_valid and nb_movement<GLOBAL_LENGTH:

            l = [move_down, move_right, move_up, move_left]
            score_tot = np.zeros(4)
            for j in range(len(l)):
                test_board, test_game_valid, test_score = l[j](search_board)
                if test_game_valid and (not egal(test_board,search_board)):
                    for _ in range(GLOBAL_LENGTH):
                        search_board2 = np.copy(test_board)
                        search_board2 = add_new_tile(search_board2)
                        score_tot[j] += test_score
                        nb_move = 0
                        game_valid2 = True
                        while game_valid2 and nb_move<GLOBAL_LENGTH:
                            search_board2, game_valid2, score2 = random_move(search_board2)
                            nb_move += 1
                            if game_valid2:
                                search_board2 = add_new_tile(search_board2)
                                score_tot[j] += score2
                    score_tot[j] /= GLOBAL_LENGTH

            search_board, game_valid, score = l[np.argmax(score_tot)](search_board)
            if game_valid:
                search_board = add_new_tile(search_board)
                tot_score += score
            
            while game_valid:
                search_board, game_valid, score = random_move(search_board)
                if game_valid:
                    search_board = add_new_tile(search_board)
                    tot_score += score

    return tot_score/nb_w


def UCS(board_with_first_move):
    tot_score = 0
    nb_w1 = 0
    time0 = time.time()
    while time.time()-time0<TIME_ONE_MOVE/NUMBER_OF_MOVES:
        nb_w1 += 1
        search_board = np.copy(board_with_first_move)
        search_board = add_new_tile(search_board)
        score = np.exp(0/4096 - 0.5)
        Q = [(1, search_board, score)]
        ok=True
        score1 = 0
        while ok and len(Q)>0:
            score_max = 0
            l_ind_max = []
            for i in range(len(Q)):
                move_number, test_board, score = Q[i]
                if score>score_max:
                    l_ind_max=[i]
                    score_max = score
                elif score==score_max:
                    l_ind_max.append(i)
            ind_max = rd.choice(l_ind_max)
            move_number, search_board, score = Q.pop(ind_max)
            if move_number==GLOBAL_LENGTH:
                score1 = int(4096*(np.log(score)+GLOBAL_LENGTH)-GLOBAL_LENGTH*2048)
                ok=False
            if ok:
                for f in [move_left, move_up, move_down, move_right]:
                    test_board, test_game_valid, test_score = f(search_board)
                    if test_game_valid:
                        test_board = add_new_tile(test_board)
                        Q.append((move_number+1, test_board, score*np.exp(test_score/4096-0.5)))
                    else:
                        Q.append((move_number+1, test_board, score*np.exp(0/4096-0.5)))
        nb_w2 = 0
        score2 = 0
        time1 = time.time()
        while time.time()-time1<TIME_ONE_MOVE/(21*NUMBER_OF_MOVES):
            nb_w2 += 1
            search_board2 = np.copy(search_board)
            game_valid = True
            while game_valid:
                search_board2, game_valid, score = random_move(search_board2)
                if game_valid:
                    search_board2 = add_new_tile(search_board2)
                    score2 += score
        tot_score += score1+score2/nb_w2
        
    return tot_score/nb_w1  
    

def egal(n,m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            if n[i][j] != m[i][j]:
                return False
    return True


def ai_move(board):

    possible_first_moves = [move_left, move_up, move_down, move_right]
    first_move_scores = np.zeros(NUMBER_OF_MOVES)
    for first_move_index in range(NUMBER_OF_MOVES):
        first_move_function =  possible_first_moves[first_move_index]
        board_with_first_move, first_move_made, first_move_score = first_move_function(board)
        if first_move_made and (not egal(board,board_with_first_move)):
            first_move_scores[first_move_index] += first_move_score

            if USED_METHOD==0:
                first_move_scores[first_move_index] += purRandom(board_with_first_move)
            elif USED_METHOD==1:
                first_move_scores[first_move_index] += monteCarloSearch(board_with_first_move)
            elif USED_METHOD==2:
                first_move_scores[first_move_index] += greedySearch(board_with_first_move)
            elif USED_METHOD==3:
                first_move_scores[first_move_index] += treeSearch(board_with_first_move)
            elif USED_METHOD==4:
                first_move_scores[first_move_index] += UCS(board_with_first_move)
            

        else:
            first_move_scores[first_move_index] = -1
        
    """
    l = []
    max_score = 0
    for i in range(len(first_move_scores)):
        if first_move_scores[i]>max_score:
            max_score=first_move_scores[i]
            l=[i]
        elif first_move_scores[i]==max_score:
            l.append(i)
    best_move_index = rd.choice(l)
    """
    best_move_index = np.argmax(first_move_scores)
    best_move = possible_first_moves[best_move_index]
    search_board, game_valid, score = best_move(board)
    return search_board, game_valid

def ai_play(board):
    move_number = 0
    valid_game = True
    while valid_game:
        move_number += 1
        board, valid_game = ai_move(board)
        if valid_game:
            board = add_two(board)
        if check_for_win(board):
            valid_game = False
        print(board)
        print(move_number)
    print(board)
    return np.amax(board)

def ai_plot(move_func):
    tick_locations = np.arange(1, 12)
    final_scores = []
    for _ in range(SAMPLE_COUNT):
        print('thing is ', _)
        board = initialize_game()
        game_is_win = ai(board)
        final_scores.append(game_is_win)
    all_counts = np.zeros(11)
    unique, counts = np.unique(np.array(final_scores), return_counts=True)
    unique = np.log2(unique).astype(int)
    index = 0

    for tick in tick_locations:
        if tick in unique:
            all_counts[tick-1] = counts[index]
            index += 1

    plt.bar(tick_locations, all_counts)
    plt.xticks(tick_locations, np.power(2, tick_locations))
    plt.xlabel("Score of Game", fontsize = 24)
    plt.ylabel(f"Frequency per {SAMPLE_COUNT} runs", fontsize = 24)
    plt.show()



	