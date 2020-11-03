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
dice_status = [0, 0, 0, 0, 0]
roll_count = 0


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
    for i in range(len(dice_status)):
        if dice_to_roll[i] == 1:
            dice_status[i] = randint(1, 6)
    return dice_status


def get_score():
    return score_board


def set_score(dice, category):
    if score_board[category] == -1:
        score_board[category] = score(dice, score_func[category])


def is_game_finished():
    if min(score_board) != -1:
        return 1
    else:
        return 0


def get_yacht_input(yacht_input):
    dice_input, score_input = yacht_input[:6], yacht_input[6:]
    print(dice_input)
    print(score_input)
