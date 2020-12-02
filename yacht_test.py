from yacht_main import score_func
from yacht_main import yacht_score
from yacht_main import dice_status_output
from random import *


def create_train_set(size_per_score_type):
    train_set = []
    for score_type in range(score_func.index(yacht_score.SIXES), score_func.index(yacht_score.YACHT) + 1):
        for i in range(size_per_score_type):
            already_set_scores = [0] * 6
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

            elif score_type != score_func.index(yacht_score.CHOICE):
                selected_number, selected_number_count = 0, 0

                while True:
                    found_number = False
                    already_set_scores = [0] * 6
                    temp_bonus_total = 0
                    number_index = [1, 2, 3, 4, 5, 6]
                    shuffle(number_index)
                    for number in number_index:
                        randomizer = random()

                        if randomizer < 0.05:
                            number_count = 0
                        elif randomizer < 0.1:
                            number_count = 1
                        elif randomizer < 0.15:
                            number_count = 2
                        elif randomizer < 0.525:
                            number_count = 3
                        elif randomizer < 0.90:
                            number_count = 4
                        else:
                            number_count = 5

                        temp_bonus_total += number_count * number
                        if temp_bonus_total >= 63:
                            selected_number = number
                            selected_number_count = number_count
                            found_number = True
                            break
                        else:
                            already_set_scores[number - 1] = 1
                    if found_number:
                        break

                selected_number_index = sample(range(0, 5), selected_number_count)
                for dice_index in range(0, 5):
                    if dice_index in selected_number_index:
                        raw_dice_state[dice_index] = selected_number
                    else:
                        raw_dice_state[dice_index] = choice([k for k in [1, 2, 3, 4, 5, 6] if k != selected_number])

            score_state = [0] * 12
            for score_state_index in range(len(score_state)):
                if score_state_index < len(already_set_scores):
                    score_state[score_state_index] = already_set_scores[score_state_index]
                elif score_state_index != score_type:
                    score_state[score_state_index] = randint(0, 1)
                else:
                    score_state[score_state_index] = 0

            roll_count_state = [randint(0, 2)]
            dice_state = dice_status_output(raw_dice_state)

            bonus_score = 0
            for upper_scores in range(score_func.index(yacht_score.ONES), score_func.index(yacht_score.SIXES) + 1):
                bonus_score += randint(1, 6) * score_state[upper_scores]
            bonus_state = [bonus_score]
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

