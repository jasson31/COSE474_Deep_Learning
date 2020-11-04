from random import randint
from enum import Enum
import yacht_score
from yacht_score import score

# Each score board element stands for :
# ONES, TWOS, THREES, FOURS, FIVES, SIXES, CHOICE, FOUR_OF_A_KIND, FULL_HOUSE, SMALL_STRAIGHT, LARGE_STRAIGHT, YACHT
score_board = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
score_func = [yacht_score.ONES, yacht_score.TWOS, yacht_score.THREES, yacht_score.FOURS, yacht_score.FIVES,
              yacht_score.SIXES, yacht_score.CHOICE, yacht_score.FOUR_OF_A_KIND, yacht_score.FULL_HOUSE,
              yacht_score.SMALL_STRAIGHT, yacht_score.LARGE_STRAIGHT, yacht_score.YACHT]
dice_status = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
roll_count, total_score = 2, 0


class Color(Enum):
    ONES = 0
    TWOS = 1
    THREES = 2
    FOURS = 3
    FIVES = 4
    SIXES = 5
    CHOICE = 6
    FOUR_OF_A_KIND = 7
    FULL_HOUSE = 8
    SMALL_STRAIGHT = 9
    LARGE_STRAIGHT = 10
    YACHT = 11


def roll_dice(dice_to_roll):
    global roll_count
    for i in range(len(dice_status)):
        if dice_to_roll[i] > 0:
            dice_status[i] = randint(1, 6)
    roll_count -= 1
    return dice_status


def get_yacht_output():
    return score_board + [roll_count] + dice_status


def set_score(dice, category):
    if score_board[category] == -1:
        score_board[category] = score(dice, score_func[category])


def is_game_finished():
    return -1 not in score_board


def update(yacht_input):
    global roll_count, total_score
    dice_input, score_input = yacht_input[:6], yacht_input[6:]
    if roll_count > 0 and not dice_input <= [0, 0, 0, 0, 0]:  # Roll dice
        roll_dice(dice_input)
    elif not is_game_finished():  # Set score
        print(score_input.index(max(score_input)))
        set_score(score_input, score_input.index(max(score_input)))
        roll_count = 3
        roll_dice([1, 1, 1, 1, 1])
    else:  # Game Ended
        bonus_counter = 0
        for i in score_board:
            total_score += i
            if i < 6:
                bonus_counter += i
        if bonus_counter >= 63:
            total_score += 35

        print('Game End')
        print(total_score)
