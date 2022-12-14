from typing import * 
import json 
from functools import cmp_to_key

"""No numpy today since it's like a nesting algo. lol"""

TEST_FILE = "day13/test_input.txt"
INPUT_FILE = "day13/input.txt"

STOP_IN_ORDER = -1
STOP_OUT_ORDER = 1
STOP_CONTINUE = 0

DIVIDER_PACKET1 = [[2]]
DIVIDER_PACKET2 = [[6]]

def read_stuff(filename) -> List:
    packet_pairs = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        i = 0 
        while i < len(lines):
            line1 = json.loads(lines[i].strip())
            line2 = json.loads(lines[i + 1].strip())
            packet_pairs.append((line1, line2))
            i += 3
    return packet_pairs

def is_right_order(left, right):
    """Invariant, left and right are the same types."""
    if not isinstance(left, List):
        # number base case 
        if left < right:
            return STOP_IN_ORDER
        elif left > right:
            return STOP_OUT_ORDER
        else:
            return STOP_CONTINUE

    # handle list case 
    left_i = 0
    right_i = 0
    while left_i < len(left) and right_i < len(right):
        cur_left = left[left_i]
        cur_right = right[right_i]

        if type(cur_left) == type(cur_right):
            comparison = is_right_order(cur_left, cur_right)
        else:
            if not isinstance(cur_left, list):
                cur_left = [cur_left]
            if not isinstance(cur_right, list):
                cur_right = [cur_right]
            comparison = is_right_order(cur_left, cur_right)

        if comparison != STOP_CONTINUE:
            return comparison

        left_i += 1
        right_i += 1

    if len(left) < len(right):
        return STOP_IN_ORDER
    elif len(left) > len(right):
        return STOP_OUT_ORDER
    else:
        return STOP_CONTINUE

if __name__ == "__main__":
    # part 1
    packet_pairs = read_stuff(INPUT_FILE)
    p1_ans = 0
    for i, (left, right) in enumerate(packet_pairs):
        index = i + 1
        return_code = is_right_order(left, right)
        if return_code == STOP_IN_ORDER:
            p1_ans += index 
    print(p1_ans)

    # part 2
    all_packets = []
    for packet1, packet2 in packet_pairs:
        all_packets.append(packet1)
        all_packets.append(packet2)
    all_packets.append(DIVIDER_PACKET1)
    all_packets.append(DIVIDER_PACKET2)
    all_packets.sort(key=cmp_to_key(is_right_order))
    p2_ans = 1
    for i, packet in enumerate(all_packets):
        index = i + 1
        if packet in [DIVIDER_PACKET1, DIVIDER_PACKET2]:
            p2_ans *= index 
    print(p2_ans)