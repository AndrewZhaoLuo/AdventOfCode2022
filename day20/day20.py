import numpy as np 
from typing import *
from collections import defaultdict
import re
import math 

TEST_FILE = "day20/test_input.txt"
INPUT_FILE = "day20/input.txt"

NEXT = 0
PREV = 1
DATA = 2

def read_stuff(filename) -> List:
    with open(filename, 'r') as f:
        lines = f.readlines()
        return np.array([int(l.strip()) for l in lines], dtype='int64')

def mix(initial_list: np.ndarray, num_times=1):
    N = len(initial_list)
    
    # constant space for linked list nodes
    # the way it works is 
    # row 0 --> index into next node (indexing based on col in list)
    # row 1 --> index into prev node
    # row 2 --> original data
    linked_list = np.zeros((3, N), dtype="int64")
    linked_list[NEXT, :] = (np.array(range(N)) + 1) % N 
    linked_list[PREV, :] = (np.array(range(N)) - 1 + N) % N
    linked_list[DATA, :] = initial_list

    def normalize_offset(i):
        if i == 0:
            return 0 
        return int(i % ((N - 1) * np.sign(i)))

    def shift_once(mem_index_left, mem_index_right):
        ## x <-> left <-> right <-> y goes to 
        ## x <-> right <-> left <-> y 
        left_node = linked_list[:, mem_index_left]
        right_node = linked_list[:, mem_index_right]

        left_left_node = linked_list[:, left_node[PREV]]
        right_right_node = linked_list[:, right_node[NEXT]]

        left_left_node[NEXT] = mem_index_right
        right_right_node[PREV] = mem_index_left

        # writing to slice writes to original
        tmp = left_node[PREV]
        left_node[NEXT] = right_node[NEXT]
        left_node[PREV] = mem_index_right
        right_node[NEXT] = mem_index_left
        right_node[PREV] = tmp 

    def shift(original_index):
        cur_index = original_index
        initial_shift = normalize_offset(linked_list[DATA, cur_index])

        while initial_shift > 0:
            shift_once(original_index, linked_list[NEXT, original_index])
            initial_shift -= 1
        while initial_shift < 0:
            shift_once(linked_list[PREV, original_index], cur_index)
            initial_shift += 1

    def get_state():
        start = 0 
        next = None 
        result = []
        while next != start:
            if next is None:
                next = start
            cur_node = linked_list[:, next]
            result.append(cur_node[DATA])
            next = cur_node[NEXT]
        return result 

    for outer in range(num_times):
        for i in range(N):
            shift(i)
    return get_state()

def p1_mix(initial_list: np.ndarray):
    N = len(initial_list)
    state = mix(initial_list)
    zero_index = state.index(0)
    p1_ans = 0
    for i in [1000, 2000, 3000]:
        i = i % N
        loc = (zero_index + i) % N 
        p1_ans += state[loc]
    return p1_ans

def p2_mix(initial_list: np.ndarray):
    N = len(initial_list)
    state = mix(initial_list, num_times=10)
    zero_index = state.index(0)
    p1_ans = 0
    for i in [1000, 2000, 3000]:
        i = i % N
        loc = (zero_index + i) % N 
        p1_ans += state[loc]
    return p1_ans


if __name__ == "__main__":
    data = read_stuff(INPUT_FILE)
    # part 1
    print(p1_mix(data))
    print(p2_mix(data * 811589153))
