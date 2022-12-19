import numpy as np 
from typing import *
from collections import defaultdict

TEST_FILE = "day18/test_input.txt"
INPUT_FILE = "day18/input.txt"

def read_stuff(filename) -> List:
    points = set()
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            x, y, z = line.split(',')
            point = (int(x), int(y), int(z))
            points.add(point)
    return points 

def p1(points):
    surface_area = 0
    for point in points:
        x, y, z = point
        for neighbor in [
            (x + 1, y, z),
            (x - 1, y, z), 
            (x, y + 1, z), 
            (x, y - 1, z), 
            (x, y, z + 1), 
            (x, y, z - 1)
        ]:
            if neighbor not in points:
                surface_area += 1
    return surface_area


def p2(points, bound_upper=20, bound_lower=-5):
    start_point = (bound_lower, bound_lower, bound_lower)
    air_reachable_points = set()
    frontier = [start_point]

    while len(frontier) > 0:
        point = frontier.pop()
        if point[0] < bound_lower or point[0] > bound_upper or (
            point[1] < bound_lower or point[1] > bound_upper
        ) or (
            point[2] < bound_lower or point[2] > bound_upper
        ):
            continue 

        if point in points or point in air_reachable_points:
            continue

        air_reachable_points.add(point)
        x, y, z = point
        for neighbor in [
            (x + 1, y, z),
            (x - 1, y, z), 
            (x, y + 1, z), 
            (x, y - 1, z), 
            (x, y, z + 1), 
            (x, y, z - 1)
        ]:
            frontier.append(neighbor)
        
    surface_area = 0
    for point in points:
        x, y, z = point
        for neighbor in [
            (x + 1, y, z),
            (x - 1, y, z), 
            (x, y + 1, z), 
            (x, y - 1, z), 
            (x, y, z + 1), 
            (x, y, z - 1)
        ]:
            if neighbor not in points and neighbor in air_reachable_points:
                surface_area += 1
    return surface_area


if __name__ == "__main__":
    # part 1
    points = read_stuff(INPUT_FILE)
    print(p1(points))
    print(p2(points))