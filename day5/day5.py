import numpy as np
from typing import * 

TEST_FILE = "day5/test_input.txt"
INPUT_FILE = "day5/input.txt"

def read_stuff(filename) -> np.ndarray:
    with open(filename, 'r') as f:
        lines = f.readlines()

        # find the lines for creates 
        delimiter = lines.index('\n')
        
        crate_lines = lines[:delimiter]
        crates_lines_bottom_up = crate_lines[::-1][1:]

        max_height = len(crate_lines) * len(crate_lines[0]) // 3

        crates = [
            [ord(c) if c != ' '  else 0 for c in crate_line[1:-1:4]]
            for crate_line in crates_lines_bottom_up
        ]
        crates += max_height * [[0] * len(crates[0])]

        instructions_lines = lines[delimiter+1:]
        instructions = [
            line.split(' ') for line in instructions_lines
        ]
        instructions = [
            [int(l[1]), int(l[3]) - 1, int(l[5]) - 1] for l in instructions
        ]

    return np.array(crates).T, np.array(instructions)

def move_one_step(crate_arr, instruction):
    num_crates, src, dst = instruction
    for _ in range(num_crates):
        top_src_i = np.argwhere(crate_arr[src] == 0).min()
        top_dst_i = np.argwhere(crate_arr[dst] == 0).min()
        crate_arr[dst][top_dst_i] = crate_arr[src][top_src_i - 1]
        crate_arr[src][top_src_i - 1] = 0 

def move_one_step2(crate_arr, instruction):
    num_crates, src, dst = instruction

    top_src_i = np.argwhere(crate_arr[src] == 0).min()
    top_dst_i = np.argwhere(crate_arr[dst] == 0).min()
    crate_arr[dst][top_dst_i:top_dst_i+num_crates] = crate_arr[src][top_src_i-num_crates:top_src_i]
    crate_arr[src][top_src_i-num_crates:top_src_i] = 0 

if __name__ == "__main__":
    FILE = INPUT_FILE
    # part 1
    crate_arr, instructions = read_stuff(FILE)

    for instr in instructions:
        move_one_step(crate_arr, instr)

    msg = [chr(r[np.argwhere(r > 0).max()]) for r in crate_arr]
    print(''.join(msg))

    # part 2
    crate_arr, instructions = read_stuff(FILE)

    for instr in instructions:
        move_one_step2(crate_arr, instr)

    msg = [chr(r[np.argwhere(r > 0).max()]) for r in crate_arr]
    print(''.join(msg))