import numpy as np 
from typing import *
from collections import defaultdict
import re
import math 

TEST_FILE = "day21/test_input.txt"
INPUT_FILE = "day21/input.txt"


def read_stuff(filename) -> List:
    data = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            left, right = line.split(': ')
            expression = right.split(' ')

            if len(expression) == 1:
                data[left] = [int(expression[0])]
            else:
                data[left] = expression
    return data 

def get_topological_order(data):
    flow_graph = defaultdict(list)

    frontier = Deque([]) 
    for name, dependencies in data.items():
        if len(dependencies) > 1:
            flow_graph[dependencies[0]].append(name)
            flow_graph[dependencies[2]].append(name)
        else:
            frontier.append(name)
    
    sorted_order = []
    visited = set()
    while len(frontier) > 0:
        cur_node = frontier.popleft()
        sorted_order.append(cur_node)
        visited.add(cur_node)

        for dependency in flow_graph[cur_node]:
            assert len(data[dependency]) == 3
            left = data[dependency][0]
            right = data[dependency][2]
            if left in visited and right in visited:
                frontier.append(dependency)

    return sorted_order

def run_data(data):
    values = {}
    ordering = get_topological_order(data)
    for v in ordering:
        if len(data[v]) == 1:
            values[v] = data[v][0]
        else:
            left = values[data[v][0]]
            right = values[data[v][2]]
            operator = data[v][1]
            if operator == '+':
                result = left + right 
            elif operator == '*':
                result = left * right 
            elif operator == '-':
                result = left - right 
            elif operator == '/':
                result = left // right 
            else:
                raise ValueError(f"Unknown operator {operator}")
            values[v] = result 
    return values

def run_guess(data, guess):
    data = dict(data)
    data['humn'] = [guess]
    result = run_data(data)
    left, right = data['root'][0], data['root'][2]
    return result[left], result[right]

if __name__ == "__main__":
    # p1 data 
    data = read_stuff(INPUT_FILE)
    result = run_data(data)
    print(result['root'])

    # p2 data 
    # manual binary search
    # Between 1e12 and 1e13
    low = int(1)     # TOO BIG
    high = int(1e15) # TOO SMALL
    while low < high:
        mid = (low + high) // 2
        guess = run_guess(data, mid)

        if guess[0] < guess[1]:
            # TOO SMALL, need to decrease guesses
            high = mid 
        elif guess[0] > guess[1]:
            # TOO BIG, need to increase guesses
            low = mid 
        else:
            print("ANSWER:", mid)
            break

    print(run_guess(data, 3759569926192))