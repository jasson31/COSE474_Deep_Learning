from random import randint
import yacht_score
from yacht_score import score
import math

score_board = [[0]*12]*2
score_func = [yacht_score.ONES, yacht_score.TWOS, yacht_score.THREES, yacht_score.FOURS, yacht_score.FIVES,
              yacht_score.SIXES, yacht_score.CHOICE, yacht_score.FOUR_OF_A_KIND, yacht_score.FULL_HOUSE,
              yacht_score.SMALL_STRAIGHT, yacht_score.LARGE_STRAIGHT, yacht_score.YACHT]
dice_status = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
roll_count = 2
score_total = [0, 0]
bonus_total = [0, 0]
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


def dice_status_output(raw_dice_status):
    l = [0]*30
    for i in range(5):
        l[i*6+raw_dice_status[i]-1] += 1
    return l


def get_available_input():
    dice_action, score_action = [1] * 31, [1] * 12
    if roll_count == 0:
        dice_action = [0] * 31
    for i in range(len(score_board[cur_player])):
        if score_board[cur_player][i] == 1:
            score_action[i] = 0
    return dice_action + score_action


def get_yacht_output():
    if multi_mode:
        return score_board[cur_player] + score_board[int(not cur_player)] + [roll_count]\
               + dice_status_output(dice_status) + bonus_total, score_total, is_game_finished(), get_available_input()
    else:
        return score_board[cur_player] + [roll_count / 2] + dice_status_output(dice_status) + [min(bonus_total[cur_player], 35) / 35],\
               score_total[cur_player], is_game_finished(), get_available_input()
    
def get_yacht_output_test():
    return score_board[cur_player] +['asdf'] + [roll_count] +['asdf'] + dice_status +['asdf'] + [bonus_total[cur_player]],\
               score_total[cur_player], is_game_finished(), get_available_input()
    


def set_multi_mode(mode):
    global multi_mode
    multi_mode = mode


def set_score(dice, category):
    added_score = score(dice, score_func[category])
    
    score_board[cur_player][category] = 1
    score_total[cur_player] += added_score
    if category<6:
        bonus_total[cur_player] += added_score
    return


def is_game_finished():
    return 0 not in score_board[cur_player]


def cheated():
    for i in range(len(score_board[cur_player])):
        if score_board[cur_player][i] == 0:
            score_board[cur_player][i] = -1


def update(command_index):
    global roll_count, score_total, cur_player
    if is_game_finished():
        #print('Game End')
        #print('player : ', cur_player, ' total score : ', score_total[cur_player])
        if multi_mode:
            cur_player = int(not cur_player)
    else:
        #command_index = yacht_input.index(max(yacht_input))
        
        if command_index < 31:
            if roll_count == 0:
                cheated()
                return
            else:
                roll_dice(command_index+1)
                return
        else:
            score_index = command_index - 31
            #print(str(score_index))
            if score_board[cur_player][score_index] != 0:
                cheated()
            else:
                set_score(dice_status, score_index)
            
            roll_count = 3
            roll_dice(31)
            
            if is_game_finished():  # Game Ended

                if bonus_total[cur_player] >= 63:
                    score_total[cur_player] += 35
                
                #print('player : ', cur_player, ' total score : ', score_sum)
            if multi_mode:
                cur_player = int(not cur_player)



def reset_game():
    global score_board, dice_status, roll_count, score_total, cur_player, bonus_total
    score_board = [[0]*12]*2
    dice_status = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
    roll_count = 2
    score_total = [0, 0]
    bonus_total = [0, 0]
    cur_player = 0