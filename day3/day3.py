import numpy as np
from typing import * 

TEST_FILE = "day3/test_input.txt"
INPUT_FILE = "day3/input.txt"

def get_priority(c: str):
    if c.isupper():
        return ord(c) - ord('A') + 27
    return ord(c) - ord('a') + 1

def read_stuff(filename) -> List[np.ndarray]:
    sacks: List[np.ndarray] = []

    with open(filename, 'r') as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()
            res = [get_priority(c) for c in line]
            res = np.array(res)
            sacks.append(res)

    return sacks

def find_commonality(sack: np.ndarray) -> int:
    left, right = sack[:len(sack) // 2], sack[len(sack) // 2:]
    return np.intersect1d(left, right)

def find_group_priority(sack1: np.ndarray, sack2: np.ndarray, sack3: np.ndarray) -> int:
    common1 = np.intersect1d(sack1, sack2)
    return np.intersect1d(common1, sack3)

if __name__ == "__main__":
    # part 1
    encoding = read_stuff(INPUT_FILE)
    sum_part1 = 0
    for sack in encoding:
        sum_part1 += find_commonality(sack)
    print(sum_part1)

    # part 2 
    sum_part2 = 0
    for i in range(len(encoding) // 3):
        sack1, sack2, sack3 = encoding[i * 3: i * 3 + 3]
        sum_part2 += find_group_priority(sack1, sack2, sack3)
    print(sum_part2)