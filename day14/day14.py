from typing import * 
from collections import defaultdict

"""No numpy today since it's like a nesting algo. lol"""

TEST_FILE = "day14/test_input.txt"
INPUT_FILE = "day14/input.txt"

def get_points(r1, c1, r2, c2):
    points = []
    r_start = min(r1, r2)
    r_end = max(r1, r2)
    c_start = min(c1, c2)
    c_end = max(c1, c2)

    dr = r_end - r_start 
    dc = c_end - c_start 

    while dr >= 0:
        points.append((c_start, r_start + dr))
        dr -= 1
    while dc >= 0:
        points.append((c_start + dc, r_start))
        dc -= 1

    return points 

def read_stuff(filename) -> List:
    rows_to_blocked_cols = defaultdict(set)
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            pairs = line.strip().split('->')
            pairs = [p.strip().split(',') for p in pairs]
            pairs = [(int(p[0]), int(p[1])) for p in pairs]
            for i in range(len(pairs) - 1):
                p1 = pairs[i]
                p2 = pairs[i + 1]
                for c, r in get_points(p1[1], p1[0], p2[1], p2[0]):
                     rows_to_blocked_cols[r].add(c)
    return rows_to_blocked_cols


if __name__ == "__main__":
    # part 1
    rows_to_blocked_cols = read_stuff(INPUT_FILE)
    biggest_row = max(rows_to_blocked_cols.keys())
    sand_start = (500, 0)

    rows_to_blocked_cols_sand = defaultdict(set)

    def is_blocked(row, col):
        return col in rows_to_blocked_cols[row] or col in rows_to_blocked_cols_sand[row]

    num_sand = 0
    while True:
        cur_col, cur_row = sand_start
        is_settled = False 
        while cur_row < biggest_row and not is_settled:
            next_points = [(cur_row + 1, cur_col), (cur_row + 1, cur_col - 1), (cur_row + 1, cur_col + 1)]
            is_settled = True 
            for next_row, next_col in next_points:
                if not is_blocked(next_row, next_col):
                    cur_row = next_row
                    cur_col = next_col
                    is_settled = False
                    break 
        if is_settled:
            num_sand += 1
            rows_to_blocked_cols_sand[cur_row].add(cur_col)
        else:
            break 
    print(num_sand)

    # part 2

    rows_to_blocked_cols_sand = defaultdict(set)
    def is_blocked(row, col):
        return col in rows_to_blocked_cols[row] or col in rows_to_blocked_cols_sand[row] or row >= biggest_row + 2

    num_sand = 0
    while not is_blocked(0, 500):
        cur_col, cur_row = sand_start
        is_settled = False 
        while not is_settled:
            next_points = [(cur_row + 1, cur_col), (cur_row + 1, cur_col - 1), (cur_row + 1, cur_col + 1)]
            is_settled = True 
            for next_row, next_col in next_points:
                if not is_blocked(next_row, next_col):
                    cur_row = next_row
                    cur_col = next_col
                    is_settled = False
                    break 
        if is_settled:
            num_sand += 1
            rows_to_blocked_cols_sand[cur_row].add(cur_col)
        else:
            break 
    print(num_sand)