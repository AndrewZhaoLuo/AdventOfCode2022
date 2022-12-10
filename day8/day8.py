import numpy as np
from typing import * 

TEST_FILE = "day8/test_input.txt"
INPUT_FILE = "day8/input.txt"

def read_stuff(filename) -> np.ndarray:
    grid = [] 
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            tree_row = []
            for c in line.strip():
                tree_row.append(int(c))
            grid.append(tree_row)
    return np.array(grid)
    
def get_scenic_score_direction(arr: np.ndarray, axis: int):
    # The idea is to loop over all possible values for tree heights
    # Let's say we have tree height h we are considering
    # for every element along our axis equal to h, we want to find the biggest index
    # less than the index at h along the axis. 
    indices_array = np.indices(arr.shape)[axis]

    '''
    scenic_scores = np.zeros_like(arr)
    for h in range(0, 10):
        taller_than = (arr >= h)
        indices_of_interest = indices_array * taller_than
        indices_of_interest = np.maximum.accumulate(indices_of_interest, axis=axis)

        # boolean mask of current places of interest
        arr_of_interest = arr == h 
        height_diff = indices_array - np.roll(indices_of_interest, 1, axis=axis)
        height_diff[height_diff < 0] = 0
        result_local = height_diff * arr_of_interest
        scenic_scores += result_local
    '''
    # Vectorized version of the above, first dim is now h
    arr_stacked = np.repeat(arr[:,:,None], 10, axis=2).transpose([2, 0, 1])
    height_array = np.array(range(10)).reshape([10, 1, 1])
    taller_than = arr_stacked >= height_array
    indices_of_interest = indices_array[None, :, :] * taller_than
    indices_of_interest = np.maximum.accumulate(indices_of_interest, axis=axis+1)
    arr_of_interest = arr_stacked == height_array
    height_diff = indices_array - np.roll(indices_of_interest, 1, axis=axis+1)
    height_diff[height_diff < 0] = 0
    result = arr_of_interest * height_diff
    scenic_scores = result.sum(0)
    return scenic_scores

if __name__ == "__main__":
    # part 1
    tree_grid = read_stuff(INPUT_FILE)
    padded_tree_grid = np.pad(tree_grid, ((1, 1), (1, 1)), 'constant', constant_values=-1)

    # tree height seen at the grid points from relevant edge
    left_highest = np.maximum.accumulate(padded_tree_grid, axis=1)
    right_highest = np.maximum.accumulate(padded_tree_grid[:, ::-1], axis=1)[:, ::-1]
    up_highest = np.maximum.accumulate(padded_tree_grid, axis=0)
    down_highest = np.maximum.accumulate(padded_tree_grid[::-1, :], axis=0)[::-1, :]

    left_visible = np.roll(left_highest, shift=1, axis=1) < left_highest
    right_visible = np.roll(right_highest, shift=-1,axis=1) < right_highest
    up_visible = np.roll(up_highest, shift=1, axis=0) < up_highest
    down_visible = np.roll(down_highest, shift=-1, axis=0) < down_highest

    visible = (left_visible | right_visible | up_visible | down_visible)
    print(visible.flatten().sum())

    # part 2
    # helpful to have the constant value be large number
    tree_grid_p2 = tree_grid.copy()
    up_scores = get_scenic_score_direction(tree_grid_p2, 0)
    down_scores = get_scenic_score_direction(tree_grid_p2[::-1, :], 0)[::-1, :]
    left_scores = get_scenic_score_direction(tree_grid_p2, 1)
    right_scores = get_scenic_score_direction(tree_grid_p2[:, ::-1], 1)[:, ::-1]

    total_scores = up_scores * down_scores * left_scores * right_scores
    print(total_scores.max(axis=None))