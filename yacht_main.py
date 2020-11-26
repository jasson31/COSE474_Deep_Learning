from random import randint
import yacht_score
from yacht_score import score
import math

score_board = [[-10]*12]*2
score_func = [yacht_score.ONES, yacht_score.TWOS, yacht_score.THREES, yacht_score.FOURS, yacht_score.FIVES,
              yacht_score.SIXES, yacht_score.CHOICE, yacht_score.FOUR_OF_A_KIND, yacht_score.FULL_HOUSE,
              yacht_score.SMALL_STRAIGHT, yacht_score.LARGE_STRAIGHT, yacht_score.YACHT]
dice_status = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
roll_count = 2
total_score = [0, 0]
cur_player = 0
multi_mode = False


def roll_dice(roll_action_num):
    global roll_count
    for i in range(5):
        if roll_action_num % 2 == 1:
            dice_status[i] = randint(1, 6)
        roll_action_num = roll_action_num // 2
    roll_count -= 1
    return dice_status


def dice_status_output():
    l = [0]*30
    for i in range(5):
        l[i*5+dice_status[i]]+=10
    return l

def get_yacht_output():
    cur_total_score = 0
    for i in range(len(score_board[cur_player])):
        cur_total_score += score_board[cur_player][i]
        #if score_board[cur_player][i] == -10:
        #    cur_total_score += 10
    if multi_mode:
        return score_board[cur_player] + score_board[int(not cur_player)] + [roll_count] + dice_status_output(), cur_total_score, is_game_finished()
    else:
        return score_board[cur_player] + [roll_count] + dice_status_output(), cur_total_score, is_game_finished()


def set_multi_mode(mode):
    global multi_mode
    multi_mode = mode


def set_score(dice, category):
    score_board[cur_player][category] = score(dice, score_func[category])


def is_game_finished():
    return -10 not in score_board[cur_player]

def cheated():
    for i in range(len(score_board[cur_player])):
        if score_board[cur_player][i] == -10:
            score_board[cur_player][i] = -11


def update(command_index):
    global roll_count, total_score, cur_player
    if is_game_finished():
        #print('Game End')
        #print('player : ', cur_player, ' total score : ', total_score[cur_player])
        if multi_mode:
            cur_player = int(not cur_player)
    else:
        #command_index = yacht_input.index(max(yacht_input))
        
        if command_index < 31:
            if roll_count == 0:
                cheated()
            else:
                roll_dice(command_index+1)
        
        else:
            score_index = command_index - 31
            #print(str(score_index))
            if score_board[cur_player][score_index] != -10:
                cheated()
            
            else:
                # Set score
                #print('player : ', cur_player, ' Set score')
                set_score(dice_status, score_index)
            
            
            roll_count = 3
            roll_dice(31)
            if is_game_finished():  # Game Ended
                #print('Game End')
                bonus_counter, score_sum = 0, 0
                for i in score_board[cur_player]:
                    score_sum += i
                    if i < 6:
                        bonus_counter += i
                if bonus_counter >= 63:
                    score_sum += 35
                total_score[cur_player] = score_sum
                #print('player : ', cur_player, ' total score : ', score_sum)

            if multi_mode:
                cur_player = int(not cur_player)


def reset_game():
    global score_board, dice_status, roll_count, total_score, cur_player
    score_board = [[-10]*12]*2
    dice_status = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
    roll_count = 2
    total_score = [0, 0]
    cur_player = 0