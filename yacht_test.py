from yacht_main import score_func
from yacht_main import yacht_score
from yacht_main import dice_status_output
from random import *


def create_train_set(size_per_score_type):
    train_set = []
    for score_type in range(score_func.index(yacht_score.FOUR_OF_A_KIND), score_func.index(yacht_score.YACHT) + 1):
        for i in range(size_per_score_type):
            raw_dice_state = [0] * 5

            if score_type == score_func.index(yacht_score.FULL_HOUSE):
                rand_number = sample(range(1, 7), 2)
                rand_2_indexes = sample(range(0, 5), 2)

                for dice_index in range(0, 5):
                    if dice_index in rand_2_indexes:
                        raw_dice_state[dice_index] = rand_number[0]
                    else:
                        raw_dice_state[dice_index] = rand_number[1]

            elif score_type == score_func.index(yacht_score.FOUR_OF_A_KIND):
                rand_number = sample(range(1, 7), 2)
                rand_1_index = randint(0, 4)

                for dice_index in range(0, 5):
                    if dice_index == rand_1_index:
                        raw_dice_state[dice_index] = rand_number[0]
                    else:
                        raw_dice_state[dice_index] = rand_number[1]

            elif score_type == score_func.index(yacht_score.SMALL_STRAIGHT):
                rand_number = randint(1, 3)
                straight_numbers = sample(range(rand_number, rand_number + 4), 4)

                if rand_number == 1:
                    straight_numbers.append(6)
                elif rand_number == 3:
                    straight_numbers.append(1)
                else:
                    straight_numbers.append(choice(straight_numbers))

                shuffle(straight_numbers)
                for dice_index in range(0, 5):
                    raw_dice_state[dice_index] = straight_numbers[dice_index]

            elif score_type == score_func.index(yacht_score.LARGE_STRAIGHT):
                rand_number = randint(1, 2)
                straight_numbers = sample(range(rand_number, rand_number + 5), 5)

                for dice_index in range(0, 5):
                    raw_dice_state[dice_index] = straight_numbers[dice_index]

            elif score_type == score_func.index(yacht_score.YACHT):
                rand_number = randint(1, 6)

                for dice_index in range(0, 5):
                    raw_dice_state[dice_index] = rand_number

            score_state = [0] * 12
            for score_state_index in range(len(score_state)):
                if score_state_index != score_type:
                    score_state[score_state_index] = randint(0, 1)
                else:
                    score_state[score_state_index] = 0

            roll_count_state = [randint(0, 2)]
            dice_state = dice_status_output(raw_dice_state)
            bonus_state = [35 * randint(0, 1)]
            state = score_state + roll_count_state + dice_state + bonus_state

            action = 31 + score_type

            new_score_state = score_state
            new_score_state[score_type] = 1
            new_dice_state = dice_status_output(
                [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)])
            new_state = new_score_state + [2] + new_dice_state + bonus_state

            step_reward = yacht_score.score(raw_dice_state, score_func[score_type])

            # print("      state : ", state)
            # print("     action : ", action)
            # print("  new_state : ", new_state)
            # print("step_reward : ", step_reward)
            train_set.append([state, action, new_state, step_reward])
    return train_set


