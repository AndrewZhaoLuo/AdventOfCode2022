import numpy as np
from typing import * 

TEST_FILE = "day11/test_input.txt"
INPUT_FILE = "day11/input.txt"


def read_stuff(filename) -> List:
    monkey_data = []
    with open(filename, 'r') as f:
        monkey_i = 0
        lines = f.readlines()
        while monkey_i * 7 < len(lines):
            monkey_start_line_index = monkey_i * 7
            # grab raw strings
            starting_items = lines[monkey_start_line_index + 1]
            operations = lines[monkey_start_line_index + 2]
            test = lines[monkey_start_line_index + 3]
            true_branch = lines[monkey_start_line_index + 4]
            false_branch = lines[monkey_start_line_index + 5]

            # go to starting items 
            # start with the numbers 
            starting_items = starting_items.strip()[16:] 
            starting_items = [int(c) for c in starting_items.split(',')]

            # start with after the '='
            operations = operations.strip().split('= ')[-1]
            operations = operations.split(' ')
            operations = [int(c) if c.isdigit() else c for c in operations]

            # test 
            test = int(test.split('by ')[-1])
            true_branch = int(true_branch.split('monkey ')[-1])
            false_branch = int(false_branch.split('monkey ')[-1])
            monkey_i += 1

            monkey_data.append(
                (starting_items, operations, test, true_branch, false_branch)
            )
    return monkey_data

def run_operations(operations, old):
    if isinstance(operations[0], int):
        left = operations[0]
    else:
        left = old 

    if isinstance(operations[-1], int):
        right = operations[-1]
    else:
        right = old 

    if operations[1] == '+':
        return left + right 
    else:
        return left * right 

def run_one_round(monkey_info, special_mod, use_p1=True):
    inspection = np.zeros(len(monkey_info))
    for i, (starting_items, operations, test, true_branch, false_branch) in enumerate(monkey_info):
        inspection[i] += len(starting_items)
        for cur_item in list(starting_items):
            starting_items.pop(0)
            new_value = run_operations(operations, cur_item)

            # relief step
            if use_p1:
                new_value = new_value // 3
            else:
                new_value = new_value % special_mod

            if new_value % test == 0:
                new_monkey = true_branch
            else:
                new_monkey = false_branch
            monkey_info[new_monkey][0].append(new_value)
    return inspection

def run_rounds(monkey_info, rounds, use_p1=True):
    inspection = np.zeros(len(monkey_info))

    special_mod = 1
    for info in monkey_info:
        special_mod *= info[2]
    for _ in range(rounds):
        inspection += run_one_round(monkey_info, special_mod, use_p1=use_p1)
    return inspection

if __name__ == "__main__":
    file = INPUT_FILE

    # part 1
    monkey_info = read_stuff(file)

    inspections = run_rounds(monkey_info, 20)
    inspections.sort()
    print(inspections[-1] * inspections[-2])

    # part 2
    monkey_info = read_stuff(file)

    inspections = run_rounds(monkey_info, 10000, False)
    inspections.sort()
    print(inspections[-1] * inspections[-2])