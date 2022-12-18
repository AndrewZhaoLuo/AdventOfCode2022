from typing import * 
from collections import defaultdict

"""No numpy today since it's like a nesting algo. lol"""

TEST_FILE = "day16/test_input.txt"
INPUT_FILE = "day16/input.txt"

def read_stuff(filename) -> List:
    # map of valveu name to flow rate + list of neighbors
    valve_info = {} 
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            valve = line.split(' ')[1]
            flow_rate = int(line.split(';')[0].split('=')[1])
            neighbors = line.split(' ')[9:]
            neighbors = [n.replace(',', '') for n in neighbors]
            valve_info[valve] = (flow_rate, neighbors)
    return valve_info

def simplify(valve_info, include = 'AA'):
    # map of A to time to get to B. Only contains 'AA' and non-zero valves
    pathing_dict = {}
    valve_flow_data = {}

    # non-zero-valves 
    valves_of_interest = []
    for valve, (flow_rate, neighbors) in valve_info.items():
        if flow_rate != 0 or valve == include:
            valves_of_interest.append(valve)
            valve_flow_data[valve] = flow_rate

    def shortest_paths(start):
        shortest_to = defaultdict(lambda: 99999999)

        search = [(start, 0)]
        while len(search) > 0:
            location, time = search.pop()
            if shortest_to[location] <= time:
                continue 

            shortest_to[location] = time 
            for neighbor in valve_info[location][1]:
                search.append((neighbor, time + 1))
        result = dict(shortest_to.items())
        result.pop(start)
        return result 

    for valve in valves_of_interest:
        pathing_dict[valve] = shortest_paths(valve)
        for k in list(pathing_dict[valve].keys()):
            if k != include and k not in valves_of_interest:
                pathing_dict[valve].pop(k)
    valve_flow_data.pop(include)
        
    return pathing_dict, valve_flow_data

def p1_search(pathing_dict, valve_flow_data):
    open_valves = set()

    def p1_recursive(time_left, location, cur_leaked) -> int:
        if time_left < 0:
            # illegal
            return 0 

        # just wait case
        best = cur_leaked

        # move to unopened valve and open the valve
        for neighbor, time_to_reach in pathing_dict[location].items():
            if neighbor in open_valves or valve_flow_data.get(neighbor, 0) == 0:
                continue
            time_to_accomplish = time_to_reach + 1
            future_time_left = time_left - time_to_accomplish
            future_leaked = cur_leaked + valve_flow_data.get(neighbor, 0) * future_time_left

            open_valves.add(neighbor)
            best = max(best, p1_recursive(future_time_left, neighbor, future_leaked))
            open_valves.remove(neighbor)

        return best 

    return p1_recursive(30, 'AA', 0)

call_cnt = 0
resets = 0
def p2_search(pathing_dict, valve_flow_data):
    valves_to_be_opened = set()
    valves_to_be_opened.add('AA')
    cache = dict()

    def p2_recursive(
        time_left, 
        dst_a, 
        dst_b, 
        time_left_a, 
        time_left_b, 
        cur_leaked, 
    ) -> int:        
        global call_cnt
        global resets 
        call_cnt += 1
        if call_cnt % 10000000 == 0:
            call_cnt = 0
            resets += 1
            print(resets)
            print(time_left, dst_a, dst_b, time_left_a, time_left_b, cur_leaked, tuple(sorted(valves_to_be_opened)))

        if time_left < 0:
            # illegal
            return 0 

        if time_left_a == float('inf') and time_left_b == float('inf'):
            # both people decide to do nothing
            return cur_leaked

        # maintain a resolves before b
        if time_left_a > time_left_b:
            return p2_recursive(time_left, dst_b, dst_a, time_left_b, time_left_a, cur_leaked)

        cache_key = (time_left, dst_a, dst_b, time_left_a, time_left_b, cur_leaked, tuple(sorted(valves_to_be_opened)))
        if cache_key in cache:
            return cache[cache_key]

        # Time is resolved for a
        time_left -= time_left_a
        cur_leaked += valve_flow_data.get(dst_a, 0) * time_left
        time_left_b -= time_left_a
        if time_left < 0:
            return 0 ## illegal, additional pruning

        best = cur_leaked
        for neighbor, time_to_reach in pathing_dict[dst_a].items():
            if neighbor in valves_to_be_opened:
                continue
            valves_to_be_opened.add(neighbor)
            best = max(best, 
                p2_recursive(
                    time_left, 
                    neighbor, 
                    dst_b, 
                    time_to_reach + 1, 
                    time_left_b, 
                    cur_leaked, 
                    )
                )
            valves_to_be_opened.remove(neighbor)

        # Here we know a is resolved, alternate case is a does nothing from now on and it's like p1 
        # But we only want to do this when there is not many valves lefet
        # It may be the case that we want go for the elephant if it is shorter
        best = max(best, p2_recursive(
            time_left, dst_b, 'AA', time_left_b, float('inf'), cur_leaked
        ))

        cache[cache_key] = best 
        return best 

    return p2_recursive(26, 'AA', 'AA', 0, 0, 0)

def p2_search_alternate(pathing_dict, valve_flow_data):

    def wrapped_call(time_left, location, cur_leaked, allowed_valves):
        open_valves = set()
        cache = dict()
        def p1_recursive(time_left, location, cur_leaked, allowed_valves) -> int:
            cached_key = (
                time_left, 
                location, 
                cur_leaked,
                tuple(sorted(allowed_valves)),
                tuple(sorted((open_valves))),
            )
            if cached_key in cache: 
                return cache[cached_key]
            if time_left < 0:
                # illegal
                return 0 

            # just wait case
            best = cur_leaked

            # move to unopened valve and open the valve
            for neighbor, time_to_reach in pathing_dict[location].items():
                if neighbor not in allowed_valves:
                    continue
                if neighbor in open_valves or valve_flow_data.get(neighbor, 0) == 0:
                    continue
                time_to_accomplish = time_to_reach + 1
                future_time_left = time_left - time_to_accomplish
                future_leaked = cur_leaked + valve_flow_data.get(neighbor, 0) * future_time_left

                open_valves.add(neighbor)
                best = max(best, p1_recursive(future_time_left, neighbor, future_leaked, allowed_valves))
                open_valves.remove(neighbor)

            cache[cached_key] = best
            return best 
        return p1_recursive(time_left, location, cur_leaked, allowed_valves)

    import itertools, time
    valves_of_interest = set(valve_flow_data.keys())
    max_values = 0
    for num_left in range(len(valves_of_interest) // 2 + 1):
        print(num_left, '/', len(valves_of_interest) // 2 + 1)
        start = time.time()
        for left_valves in itertools.permutations(valves_of_interest, num_left):
            left_valves = set(left_valves)
            right_valves = valves_of_interest - left_valves
            # print(left_valves, right_valves)
            max_values = max(
                max_values, 
                wrapped_call(26, 'AA', 0, left_valves) + wrapped_call(26, 'AA', 0, right_valves)
            )
        end = time.time()
        print('\tV:', max_values, end - start, '(s)')

    return max_values

if __name__ == "__main__":
    # part 1
    valve_info = read_stuff(INPUT_FILE)
    pathing_dict, valve_flow_data = simplify(valve_info)
    print(p1_search(pathing_dict, valve_flow_data))
    # print(p2_search(pathing_dict, valve_flow_data))
    print(p2_search_alternate(pathing_dict, valve_flow_data))