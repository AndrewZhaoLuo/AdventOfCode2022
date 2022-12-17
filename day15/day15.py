from typing import * 
from collections import defaultdict

"""No numpy today since it's like a nesting algo. lol"""

TEST_FILE = "day15/test_input.txt"
INPUT_FILE = "day15/input.txt"

def read_stuff(filename) -> List:
    sensors = []
    beacons = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            sensor_str, beacon_str = line.strip().split(':')
            sensor_coord_str = sensor_str.split(' at')[1]
            sensor_x = int(sensor_coord_str.split(',')[0].split('=')[1])
            sensor_y = int(sensor_coord_str.split(',')[1].split('=')[1])
            beacon_x = int(beacon_str.split('at ')[1].split(',')[0].split('=')[1])
            beacon_y = int(beacon_str.split('at ')[1].split(',')[1].split('=')[1])
            sensors.append((sensor_x, sensor_y))
            beacons.append((beacon_x, beacon_y))
    return sensors, beacons

def calculate_coverage(sensors, beacons, row_of_interest):
    coverage = []
    for sensor, beacon in zip(sensors, beacons):
        sensor_x, sensor_y = sensor
        beacon_x, beacon_y = beacon 

        total_distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        distance_to_row = abs(row_of_interest - sensor_y)
        horizontal_distance = total_distance - distance_to_row
        if horizontal_distance >= 0 and distance_to_row >= 0:
            coverage.append((sensor_x, horizontal_distance))
    return coverage 

def coverage_to_intervals(coverage):
    coverage = sorted(coverage)
    intervals = []

    for sensor_x, horizontal_distance in coverage:
        interval = (sensor_x - horizontal_distance, sensor_x + horizontal_distance)
        intervals.append(interval)

    # combine the intervals 
    intervals = sorted(intervals)
    combined_intervals = []
    last_interval = intervals[0]
    for cur_interval in intervals[1:]:
        if cur_interval[0] <= last_interval[1]:
            last_interval = (last_interval[0], max(cur_interval[1], last_interval[1]))
        else:
            combined_intervals.append(last_interval)
            last_interval = cur_interval
    combined_intervals.append(last_interval)
    return combined_intervals

def intervals_to_answer(combined_intervals, beacons, row_of_interest):
    total_count = 0
    for interval in combined_intervals:
        total_count += interval[1] - interval[0] + 1

    used_beacons = set()
    for beacon in beacons:
        if beacon[1] == row_of_interest and beacon not in used_beacons:
            total_count -= 1
            used_beacons.add(beacon)
    return total_count

def coverage_to_answer(coverage, beacons, row_of_interest):
    combined_intervals = coverage_to_intervals(coverage)
    return intervals_to_answer(combined_intervals, beacons, row_of_interest)


def clamp_interval(interval, left, right):
    if interval[1] < left:
        return None 
    if interval[0] > right:
        return None 
    return max(left, interval[0]), min(right, interval[1])


def p2_calculation(file, left_clamp, right_clamp):
    sensors, beacons = read_stuff(file)

    for row in range(left_clamp, right_clamp + 1):
        coverage = calculate_coverage(sensors, beacons, row)
        intervals = coverage_to_intervals(coverage)
        clamped_intervals = [] 
        for interval in intervals:
            clamped_interval = clamp_interval(interval, left_clamp, right_clamp)
            if clamped_interval:      
                clamped_intervals.append(clamped_interval)
        
        ruled_out_spots = intervals_to_answer(clamped_intervals, [], row)
        # print(row, ruled_out_spots)
        if ruled_out_spots != right_clamp - left_clamp + 1:
            # only one spot, assume it's the middle one 
            return (clamped_intervals[0][1] + 1) * 4000000 + row

    return None 

def p1_calculation(file, row_of_interest):
    sensors, beacons = read_stuff(file)

    coverage = calculate_coverage(sensors, beacons, row_of_interest)
    return (coverage_to_answer(coverage, beacons, row_of_interest))

if __name__ == "__main__":
    # part 1
    print(p1_calculation(TEST_FILE, 10))
    print(p1_calculation(INPUT_FILE, 2000000))

    ## part 2
    print(p2_calculation(TEST_FILE, 0, 20))
    print(p2_calculation(INPUT_FILE, 0, 4000000))