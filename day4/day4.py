import numpy as np
from typing import * 

TEST_FILE = "day4/test_input.txt"
INPUT_FILE = "day4/input.txt"

def read_stuff(filename) -> np.ndarray:
    assignments = []

    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            elf1, elf2 = line.strip().split(',')
            num1, num2 = elf1.split('-')
            num3, num4 = elf2.split('-')
            assignments.append(list(map(int, [num1, num2, num3, num4])))

    return np.array(assignments)

if __name__ == "__main__":
    # part 1
    encoding = read_stuff(INPUT_FILE)
    
    # sort numbers so earlier left bound elf is first 
    part1_encoding = np.reshape(encoding, [-1, 2, 2])
    ss = part1_encoding[:, 0, :] - part1_encoding[:, 1, :] 
    ss = np.logical_or(
        np.logical_and(ss[:, 0] >= 0, ss[:, 1] <= 0),
        np.logical_and(ss[:, 0] <= 0, ss[:, 1] >= 0)
    )
    print(sum(ss))

    # part 2
    no_overlap = np.logical_or(
        np.logical_and(
            part1_encoding[:, 0, 0] < part1_encoding[:, 1, 0],
            part1_encoding[:, 0, 1] < part1_encoding[:, 1, 0]
        ), np.logical_and(
            part1_encoding[:, 0, 0] > part1_encoding[:, 1, 0],
            part1_encoding[:, 0, 0] > part1_encoding[:, 1, 1]
        ) 
    )
    print(sum(1 - no_overlap))
    