import numpy as np
from typing import * 
from collections import deque, defaultdict


"""All the numpy I tried is inefficient (for obv reasons I hope) so sad :'("""

TEST_FILE = "day12/test_input.txt"
INPUT_FILE = "day12/input.txt"


def read_stuff(filename) -> List:
    elevations = []
    is_starts = []
    is_ends = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:  
            elevation_line = []
            is_start_line = []
            is_end_line = []
            line = line.strip()
            for c in line:
                is_end = 0
                is_start = 0
                if c == 'S':
                    c = 'a'
                    is_start = 1
                if c == 'E':
                    c = 'z'
                    is_end = 1
                elevation_line.append(ord(c) - ord('a'))
                is_start_line.append(is_start)
                is_end_line.append(is_end)
            elevations.append(elevation_line)
            is_starts.append(is_start_line)
            is_ends.append(is_end_line)

    return np.array(elevations), np.array(is_starts), np.array(is_ends)

def in_stuff(row, col, elevations):
    return row >= 0 and row < elevations.shape[0] and col >= 0 and col < elevations.shape[1]

if __name__ == "__main__":
    # part 1
    elevations, is_starts, is_ends = read_stuff(INPUT_FILE)

    start_row, start_col = np.where(is_starts == 1)
    start_row = start_row.item()
    start_col = start_col.item()

    end_row, end_col = np.where(is_ends == 1)
    end_row = end_row.item()
    end_col = end_col.item()


    def dist_forward(start_row, start_col, end_row, end_col):
        if not in_stuff(start_row, start_col, elevations) or not in_stuff(end_row, end_col, elevations):
            return None

        height_start = elevations[start_row, start_col]
        height_end = elevations[end_row, end_col]
        if height_end - height_start > 1:
            return None

        return 1

    shortest_dist = defaultdict(lambda: float('inf'))
    frontier = deque([(0, start_row, start_col)])
    # BFS is sufficient since path lengths is 1
    while len(frontier) > 0:
        dist_to, row, col = frontier.popleft()
        if shortest_dist[(row, col)] > dist_to:
            shortest_dist[(row, col)] = min(shortest_dist[(row, col)], dist_to)

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                dist = dist_forward(row, col, row + dr, col + dc)
                if dist is not None:
                    frontier.append((dist_to + dist, row + dr, col + dc))
    print(shortest_dist[end_row, end_col])

    p2 = 999999
    for start_row, start_col in zip(*np.where(elevations == 0)):
        shortest_dist = defaultdict(lambda: float('inf'))
        frontier = deque([(0, start_row, start_col)])
        # BFS is sufficient since path lengths is 1
        while len(frontier) > 0:
            dist_to, row, col = frontier.popleft()
            if shortest_dist[(row, col)] > dist_to:
                shortest_dist[(row, col)] = min(shortest_dist[(row, col)], dist_to)

                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    dist = dist_forward(row, col, row + dr, col + dc)
                    if dist is not None:
                        frontier.append((dist_to + dist, row + dr, col + dc))
        p2 = min(p2, shortest_dist[end_row, end_col])
    print(p2)