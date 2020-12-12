from random import randint
import yacht_score
from yacht_score import score
import math
import random

score_board = [[0]*12]*2 #0 if not scored, 1 if scored
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
        return dice_status

def dice_status_output(raw_dice_status):
    l = [0]*6
    for i in range(5):
        l[raw_dice_status[i]-1] += 1
    return l


def get_available_input():
    dice_action, score_action = [1] * 31, [1] * 12
    if roll_count == 0:
        dice_action = [0] * 31
    for i in range(len(score_board[cur_player])):
        if score_board[cur_player][i] == 1:
            score_action[i] = 0
    return dice_action + score_action

def expected_scores():
    expect = [-100]*12
    for i in range(12):
        if score_board[cur_player][i] != 0:
            continue
        expect[i] = score_func[i](dice_status)
        if i<6 and 63 > bonus_total[cur_player] >= 63-expect[i]:
            expect[i] += 35
    return expect

def get_yacht_output():
    if multi_mode:
        return
    else:
        return expected_scores() +\
               dice_status_output(dice_status) +\
              [bonus_total[cur_player], roll_count], score_total[cur_player], is_game_finished()

def set_multi_mode(mode):
    global multi_mode
    multi_mode = mode


def set_score(dice, category):
    added_score = score(dice, score_func[category])
    score_board[cur_player][category] = 1
    return added_score


def is_game_finished():
    return 0 not in score_board[cur_player]


def cheated():
    for i in range(len(score_board[cur_player])):
        if score_board[cur_player][i] == 0:
            score_board[cur_player][i] = 1


def update(command_idx):
    global roll_count, score_total, cur_player
    command_index = int(command_idx)
    
    #print("played {0}:;;".format(command_index))
    if is_game_finished():
        #print('Game End')
        #print('player : ', cur_player, ' total score : ', score_total[cur_player])
        if multi_mode:
            cur_player = int(not cur_player)
    else:
        if command_index < 31:
            if roll_count == 0:
                cheated()
                return -100
            else:
                roll_dice(command_index+1)
                return 0
        else:
            score_index = command_index - 31

            if score_board[cur_player][score_index] != 0:
                cheated()
                return -100
            else:
                added_score = set_score(dice_status, score_index)
            
            if score_index < 6:
                bonus_total[cur_player] += added_score
                if 63+added_score > bonus_total[cur_player] >= 63:
                    added_score += 35
            
            score_total[cur_player] += added_score

            roll_count = 3
            roll_dice(31)
            
            if multi_mode:
                cur_player = int(not cur_player)
            return added_score
            
            
def reset_game():
    global score_board, dice_status, roll_count, score_total, cur_player, bonus_total
    score_board = [[0]*12]*2
    dice_status = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
    roll_count = 2
    score_total = [0, 0]
    bonus_total = [0, 0]
    cur_player = 0