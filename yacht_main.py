from random import randint
from enum import Enum
import yacht_score
from yacht_score import score
import math

score_board = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
score_func = [yacht_score.ONES, yacht_score.TWOS, yacht_score.THREES, yacht_score.FOURS, yacht_score.FIVES,
              yacht_score.SIXES, yacht_score.CHOICE, yacht_score.FOUR_OF_A_KIND, yacht_score.FULL_HOUSE,
              yacht_score.SMALL_STRAIGHT, yacht_score.LARGE_STRAIGHT, yacht_score.YACHT]
dice_status = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
roll_count = 2
total_score = [0, 0]
cur_player = 0
multi_mode = False


def roll_dice(dice_to_roll):
    global roll_count
    for i in range(len(dice_status)):
        if dice_to_roll[i] > 0:
            dice_status[i] = randint(1, 6)
    roll_count -= 1
    return dice_status


def get_yacht_output():
    if multi_mode:
        return score_board[cur_player] + score_board[int(not cur_player)] + [roll_count] + dice_status
    else:
        return score_board[cur_player] + [roll_count] + dice_status


def set_multi_mode(mode):
    global multi_mode
    multi_mode = mode


def set_score(dice, category):
    score_board[cur_player][category] = score(dice, score_func[category])


def is_game_finished():
    return -1 not in score_board[cur_player]


def update(yacht_input):
    global roll_count, total_score, cur_player
    if is_game_finished():
        print('Game End')
        print('player : ', cur_player, ' total score : ', total_score[cur_player])
        if multi_mode:
            cur_player = int(not cur_player)
    else:
        dice_input, score_input = yacht_input[:5], yacht_input[5:]

        if roll_count > 0 and not dice_input <= [0, 0, 0, 0, 0]:  # Roll dice
            print('Roll dice')
            roll_dice(dice_input)

        else:  # Set score
            print('player : ', cur_player, ' Set score')
            for i in sorted(score_input, reverse=True):
                if score_board[cur_player][score_input.index(i)] == -1:
                    set_score(dice_status, score_input.index(i))
                    break
                else:
                    score_input[score_input.index(i)] = -math.inf
            roll_count = 3
            roll_dice([1, 1, 1, 1, 1])

            if is_game_finished():  # Game Ended
                print('Game End')
                bonus_counter, score_sum = 0, 0
                for i in score_board[cur_player]:
                    score_sum += i
                    if i < 6:
                        bonus_counter += i
                if bonus_counter >= 63:
                    score_sum += 35
                total_score[cur_player] = score_sum
                print('player : ', cur_player, ' total score : ', score_sum)

            if multi_mode:
                cur_player = int(not cur_player)
