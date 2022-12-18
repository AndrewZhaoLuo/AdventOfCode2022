import numpy as np 
from typing import *
from collections import defaultdict

TEST_FILE = "day17/test_input.txt"
INPUT_FILE = "day17/input.txt"

LEFT = 0
RIGHT = 1

shapes = [
    np.array([[1, 1, 1, 1]]),
    np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]),
    np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]]),
    np.array([[1, 1, 1, 1]]).transpose(),
    np.array([[1, 1], [1, 1]])
]

def read_stuff(filename) -> List:
    # map of valveu name to flow rate + list of neighbors
    data = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            for c in line:
                if c == "<":
                    data.append(LEFT)
                else:
                    data.append(RIGHT)
    return data

def intersects(shape: np.array, volcano: np.array, loc_x: int, loc_y: int):
    # loc_x and loc_y are the upper left corner of shape 
    for offset_row in range(shape.shape[0]):
        for offset_col in range(shape.shape[1]):
            volcano_y = loc_y - offset_row
            volcano_x = loc_x + offset_col
            if volcano_x < 0 or volcano_x >= volcano.shape[1]:
                return True 
            if volcano_y < 0:
                return True 
            if shape[offset_row, offset_col] and volcano[volcano_y, volcano_x]:
                return True 
    return False 

def rest(shape: np.array, volcano: np.array, loc_x: int, loc_y: int):
    # loc_x and loc_y are the upper left corner of shape 
    for offset_row in range(shape.shape[0]):
        for offset_col in range(shape.shape[1]):
            volcano_y = loc_y - offset_row
            volcano_x = loc_x + offset_col
            volcano[volcano_y, volcano_x] = volcano[volcano_y, volcano_x] or shape[offset_row, offset_col]

def run_simulation_p1(shapes, stream, num_rested_goal):
    volcano = np.zeros([4 * num_rested_goal, 7]).astype('int8')

    num_rested = 0
    shape_i = 0
    stream_i = 0
    highest_row = -1

    highest_rows = []
    while num_rested < num_rested_goal:
        shape_i_start = shape_i
        stream_i_start = stream_i
        highest_row_start = highest_row
        highest_rows.append((highest_row_start, shape_i_start, stream_i_start))

        cur_shape = shapes[shape_i]

        # upper left corner is current location
        cur_loc_x = 2
        cur_loc_y = highest_row + 3 + cur_shape.shape[0]

        while True:
            cur_stream = stream[stream_i]
            stream_i = (stream_i + 1) % len(stream)

            # handle pushing 
            if cur_stream == LEFT and not intersects(cur_shape, volcano, cur_loc_x - 1, cur_loc_y):
                cur_loc_x -= 1
            if cur_stream == RIGHT and not intersects(cur_shape, volcano, cur_loc_x + 1, cur_loc_y):
                cur_loc_x += 1

            # handle falling 
            if intersects(cur_shape, volcano, cur_loc_x, cur_loc_y - 1):
                # handle case, update highest row  
                rest(cur_shape, volcano, cur_loc_x, cur_loc_y)
                highest_row = max(highest_row, cur_loc_y)
                num_rested += 1
                # print(volcano[:highest_row + 1, :][::-1, :])
                # print(highest_row)
                # breakpoint()
                break 
            
            cur_loc_y -= 1

        shape_i = (shape_i + 1) % len(shapes)

    highest_rows.append((highest_row, shape_i, stream_i))
    return highest_rows


def run_simulation_p2(shapes, stream, num_rested_goal, cycle_finder_depth):
    ## Idea is to use cycles in shapes and stream 
    ## Once shape and stream both start at 0, check if the height of the tower 
    ## grew the same amount as the last time. If it did we can break early
    ## and multiply
    data = run_simulation_p1(shapes, stream, cycle_finder_depth)

    cache_history = defaultdict(list)
    for num_settled_before_drop, (highest_row, shape_i, stream_i) in enumerate(data):
        cache_history[(shape_i, stream_i)].append((highest_row, num_settled_before_drop))

        if len(cache_history[(shape_i, stream_i)]) == 3:
            cached_1, cached_2, cached_3 = cache_history[(shape_i, stream_i)]

            if cached_1[0] - cached_2[0] == cached_2[0] - cached_3[0] and (
                cached_1[1] - cached_2[1] == cached_2[1] - cached_3[1]
            ):
                delta_num_rocks = cached_2[1] - cached_1[1]
                delta_height = cached_2[0] - cached_1[0]

                start_num_rocks = cached_1[1]
                start_height = cached_1[0]

                cycles = (num_rested_goal - start_num_rocks) // delta_num_rocks
                rocks_after_cycles = start_num_rocks + cycles * delta_num_rocks
                height_after_cycles = start_height + cycles * delta_height

                # now calculate remaining cycles_left
                rocks_left = num_rested_goal - rocks_after_cycles
                tail_rows = data[start_num_rocks + rocks_left][0]
                row_gain = tail_rows - start_height
                return height_after_cycles + 1 + row_gain
    return None 



if __name__ == "__main__":
    # part 1
    stream = read_stuff(INPUT_FILE)
    data = run_simulation_p1(shapes, stream, 2022)
    print(data[2022 - 1][0] + 1) # +1 since zero indexed
    print(run_simulation_p2(shapes, stream, 1000000000000, 5000))