import numpy as np
from typing import * 

TEST_FILE = "day9/test_input.txt"
TEST_FILE2 = "day9/test_input2.txt"
INPUT_FILE = "day9/input.txt"

"""
Planning to do this by simulation with each time step so no real numpy :'( 
"""

MOVEMENT_MAP = {
    "R": np.array((1, 0)),
    "L": np.array((-1, 0)),
    "U": np.array((0, 1)),
    "D": np.array((0, -1)),
}

def read_stuff(filename) -> List:
    steps = [] 
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            direction, num_steps = line.split(' ')
            steps.append((direction, int(num_steps)))
    return steps
    
def is_adjacent(point_a: np.ndarray, point_b: np.ndarray):
    return (np.abs((point_a - point_b)) <= 1).all()

def calculate_next_step(point_a: np.ndarray, point_b: np.ndarray):
    # a is the leading one 
    if is_adjacent(point_a, point_b):
        return point_b

    delta = point_a - point_b
    delta[delta > 1] = 1
    delta[delta < -1] = -1
    return point_b + delta

def solve_with_segments_n(segment_num, movements):
    visited = set([(0, 0)])
    segments = [np.array((0, 0)) for _ in range(segment_num)]
    for direction, steps in movements:
        for _ in range(steps):
            segments[0] = segments[0] + MOVEMENT_MAP[direction]
            for i in range(len(segments) - 1):
                segments[i + 1] = calculate_next_step(segments[i], segments[i + 1])
            visited.add(tuple(segments[-1]))

    return len(visited)

if __name__ == "__main__":
    # part 1
    movements = read_stuff(INPUT_FILE)

    print(solve_with_segments_n(2, movements))
    print(solve_with_segments_n(10, movements))