import numpy as np
from typing import * 

TEST_FILE = "day10/test_input.txt"
INPUT_FILE = "day10/input.txt"

NOOP = "noop"
ADDX = "addx"

def read_stuff(filename) -> List:
    with open(filename, 'r') as f:
        lines = f.readlines()
        return [line.strip() for line in lines]
    
def run_instr(instr_string, cur_cycle, cur_X):
    if instr_string == NOOP:
        return [((cur_cycle + 1), cur_X)]
    else:
        num = int(instr_string.split(' ')[1])
        return [((cur_cycle + 1), cur_X), ((cur_cycle + 2), cur_X + num)]

if __name__ == "__main__":
    # part 1
    instructions = read_stuff(INPUT_FILE)
    cur_X = 1
    cur_cycle = 1
    x_end_of_cycle = [cur_X]

    p1_answer = 0
    for inst in instructions:  
        ret = run_instr(inst, cur_cycle, cur_X)
        # print(inst)
        for next_cycle, next_X in ret:
            # print('\t', next_cycle, ':', next_X)
            x_end_of_cycle.append(next_X)
            # Semantics are a little different -- oops
            if (next_cycle) in [20, 60, 100, 140, 180, 220]:
                p1_answer += (next_cycle) * next_X
        cur_cycle, cur_X = ret[-1]
    print(p1_answer)

    # part 2 answer
    answer = []
    for cur_clock in range(1, 241):
        reg_x_during_draw = x_end_of_cycle[cur_clock]
        horizontal_position = cur_clock % 40
        if abs(reg_x_during_draw - horizontal_position) <= 1:
            answer.append('#')
        else:
            answer.append('.')

    answer = np.array(answer).reshape(6, 40)
    for row in answer:
        print(''.join(row)) 