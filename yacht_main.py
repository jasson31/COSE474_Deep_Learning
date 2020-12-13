from random import randint
import yacht_score
from yacht_score import score
import math
import random

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
    dice_status.sort()
    return dice_status

def handled_roll():
    # straight_3, straight_4, straight_5, 212, fh, 311, 41, yacht
    handled_weight = [5, 3, 2, 3, 2, 4, 2, 1]
    category = random.choices(population=range(len(handled_weight)), weights=handled_weight)[0]
    # straight_3
    if category == 0:
        bot = random.randint(1, 4)
        seq = random.sample(list(range(5)), 5)
        for i in range(3):
            dice_status[seq[i]] = bot + i
        remain_value = list(range(1, 7))
        if bot - 1 > 0:
            remain_value.remove(bot -1)
        if bot + 3 < 7:
            remain_value.remove(bot + 3)
        dice_status[seq[3]] = random.choice(remain_value)
        dice_status[seq[4]] = random.choice(remain_value)
    # straight_4
    elif category == 1:
        seq = random.sample(list(range(5)), 5)
        bot = random.choice([1,3])
        for i in range(4):
            dice_status[seq[i]] = bot + i
        remain_value = list(range(1,7))
        if bot == 1:
            remain_value.remove(5)
        else:
            remain_value.remove(2)
        dice_status[seq[4]] = random.choice(remain_value)
    # straight_5
    elif category == 2:
        seq = random.sample(list(range(5)), 5)
        bot = random.randint(1,2)
        for i in range(5):
            dice_status[seq[i]] = bot + i
    # fh_212
    elif category == 3:
        seq = random.sample(list(range(5)), 5)
        fh_values = random.sample(list(range(1, 7)), k=3)
        for i in range(4):
            dice_status[seq[i]] = fh_values[i//2]
        dice_status[seq[4]] = fh_values[2]
    # fh
    elif category == 4:
        seq = random.sample(list(range(5)), 5)
        fh_values = random.sample(list(range(1, 7)), k=2)
        for i in range(4):
            dice_status[seq[i]] = fh_values[i//2]
        dice_status[seq[4]] = fh_values[1]
    # 311
    elif category == 5:
        seq = random.sample(list(range(5)), 5)
        tri_values = random.sample(list(range(1, 7)), k=3)
        for i in range(3):
            dice_status[seq[i]] = tri_values[0]
        dice_status[seq[3]] = tri_values[1]
        dice_status[seq[4]] = tri_values[2]
    # 41
    elif category == 6:
        seq = random.sample(list(range(5)), 5)
        four_values = random.sample(list(range(1, 7)), k=2)
        for i in range(5):
            dice_status[seq[i]] = four_values[i//4]
    # yacht
    elif category == 7:
        value = random.randint(1, 6)
        for i in range(5):
            dice_status[i] = value
    dice_status.sort()
    return dice_status

def expected_score():
    ret = [0] * 12
    for i in range(12):
        ret[i] = score(dice_status, score_func[i])
    return ret

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
        if score_board[cur_player][i] == 0:
            score_action[i] = 0
    return dice_action + score_action


def get_yacht_output():
    if multi_mode:
        return score_board[cur_player] + score_board[int(not cur_player)] + [roll_count]\
               + dice_status + bonus_total, score_total, is_game_finished(), get_available_input()
    else:
        score_board_output = [0] * 12

        for i in range(len(score_board_output)):
            if score_board[cur_player][i] == 0:
                score_board_output[i] = -10
            elif score_board[cur_player][i] == 1:
                score_board_output[i] = yacht_score.score(dice_status, score_func[i])
            else:
                score_board_output[i] = -1

        
        return score_board_output + [roll_count] + dice_status\
                + [bonus_total[cur_player]]+ [score_total[cur_player]],\
                 score_total[cur_player], is_game_finished(), get_available_input()


def set_multi_mode(mode):
    global multi_mode
    multi_mode = mode


def set_score(dice, category):
    added_score = score(dice, score_func[category])
    
    score_board[cur_player][category] = 0
    score_total[cur_player] += added_score
    if category<6:
        bonus_total[cur_player] += added_score
    return added_score


def is_game_finished():
    return 1 not in score_board[cur_player]


def cheated():
    for i in range(len(score_board[cur_player])):
        if score_board[cur_player][i] == 1:
            score_board[cur_player][i] = -1


def get_reward(dice_status, score_index):
    checker = yacht_score.score(dice_status, score_func[score_index])
    if score_index <= score_func.index(yacht_score.SIXES):
        if dice_status.count(score_index+1) == 0:
            return 0
        elif 1 <= dice_status.count(score_index+1) <= 2:
            return 1
        elif dice_status.count(score_index+1) == 3:
            return 2
        elif 4 <= dice_status.count(score_index+1) <= 5:
            return 3
        else:
            return 2
    elif score_index == score_func.index(yacht_score.CHOICE):
        if checker <= 10:
            return 0
        elif checker <= 20:
            return 1
        else:
            return 2
    elif score_index == score_func.index(yacht_score.FOUR_OF_A_KIND) \
            or score_index == score_func.index(yacht_score.FULL_HOUSE):
        if checker <= 10:
            return 0
        elif checker <= 15:
            return 1
        else:
            return 2
    elif score_index == score_func.index(yacht_score.SMALL_STRAIGHT) \
            or score_index == score_func.index(yacht_score.LARGE_STRAIGHT):
        if checker == 0:
            return 0
        else:
            return 2
    elif score_index == score_func.index(yacht_score.YACHT):
        if checker == 0:
            return 0.2
        else:
            return 5



def update(command_index):
    global roll_count, score_total, cur_player
    if is_game_finished():
        #print('Game End')
        #print('player : ', cur_player, ' total score : ', score_total[cur_player])
        if multi_mode:
            cur_player = int(not cur_player)
    else:
        #command_index = yacht_input.index(max(yacht_input))
        bonus_earned = bonus_total[cur_player] >= 63
        if command_index < 31:
            if roll_count == 0:
                cheated()
                return -10
            else:
                roll_dice(command_index+1)
                return 0
        else:
            score_index = command_index - 31
            #print(str(score_index))
            if score_board[cur_player][score_index] == 0:
                cheated()
                return -10
            else:
                added_score = set_score(dice_status, score_index)
            
            if not bonus_earned and bonus_total[cur_player] >= 63:
                score_total[cur_player] += 35
                added_score += 35

            reward = get_reward(dice_status, score_index)
            
            roll_count = 3
            roll_dice(31)
            
            if multi_mode:
                cur_player = int(not cur_player)
            return reward
            
            
def reset_game():
    global score_board, dice_status, roll_count, score_total, cur_player, bonus_total
    score_board = [[1]*12]*2
    dice_status = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
    dice_status.sort()
    roll_count = 2
    score_total = [0, 0]
    bonus_total = [0, 0]
    cur_player = 0
    
    
"""
상체 : 0개 0, 1~2개 0.5, 3개 1, 4~5 1.5, 6 2
초이스 : 0~10 0, 10~20, 0.5, 20~30 1
포카, 풀하 : 0 0, 1~10 0.3, 11~20 0.8, 21~30 1.3
스트 : 못먹으면 0 먹으면 1
야추 : 못먹으면 0.2 먹으면 2.5

"""