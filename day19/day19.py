import numpy as np 
from typing import *
from collections import defaultdict
import re

TEST_FILE = "day19/test_input.txt"
INPUT_FILE = "day19/input.txt"

BIG_NUM = 100000
def get_tuple(ore, clay, obsidion, geodes=0):
    return np.array((ore, clay, obsidion, geodes))

def read_stuff(filename) -> List:
    blueprints = [] 
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            cur_blueprint = []
            line = line.strip()
            nums = re.findall(r'\d+', line)
            nums = list(map(int, nums))

            # ore, clay, obsidion
            cur_blueprint.append(get_tuple(nums[1], 0, 0))
            cur_blueprint.append(get_tuple(nums[2], 0, 0))
            cur_blueprint.append(get_tuple(nums[3], nums[4], 0))
            cur_blueprint.append(get_tuple(nums[5], 0, nums[6]))

            blueprints.append(np.array(cur_blueprint))
    return blueprints

def get_build_possibilities(
    resources: np.array, 
    costs: np.array, 
    cur_robots: np.array,
    time_left: int,
) -> List[np.array]:
    possibilities = [] 

    ## insights -- only makes sense to build one robot type at a time
    ## If we build 2, then we could have built 1 in the previous time step and have more
    ## resources
    ##
    ## Because of this it never makes sense to have more robots than needed to create 
    ## any robot
    ## 
    ## We should not build nothing if we can buy a geode robot
    ##
    ## We should not build the resource robot if we could not possibly spend what we have
    ## now 

    max_costs = np.max(costs, axis=0) 

    ### try building stuff 
    can_build = (costs <= resources).all(axis=1)
        
    ### robot caps based on resource limits 
    should_build = cur_robots < max_costs + 1

    ## always build the geode ones! 
    should_build[-1] = True 

    ### calculate excess resources for all but geode
    max_build_costs = np.max(costs, 0)

    ## never cache geodes
    max_build_costs[-1] = BIG_NUM
    resource_excess = resources > (max_build_costs * time_left)
    should_build = np.logical_and(should_build, np.logical_not(resource_excess))
    good_build = can_build & should_build

    ### Always build geode crackers and obsidion
    # HACK: This one is a sus heuristic
    if good_build[-1]:
        return [
            get_tuple(0, 0, 0, 1)
        ]

    # HACK: This one is a sus heuristic
    # if good_build[-2]:
    #     return [
    #         get_tuple(0, 0, 1, 0)
    #     ]

    for i, build in enumerate(good_build):
        if build:
            build = get_tuple(0, 0, 0, 0)
            build[i] = 1 
            possibilities.append(build)
            

    # if you can build everything you can, no more waiting
    buildable_with_infinite_time = (costs <= cur_robots * BIG_NUM).all(axis=1)
    if np.logical_and(buildable_with_infinite_time, good_build).sum() < buildable_with_infinite_time.sum():
        possibilities.append(get_tuple(0, 0, 0, 0))

    return possibilities

def p1_search(
    costs,
    starting_resources=get_tuple(0, 0, 0, 0), 
    starting_robots=get_tuple(1, 0, 0, 0),
    time_max=24,
    max_frontier_length=10000,
):
    # map of (robots, time) -> list of resources there at this time step
    # this is used for pruning, if there is a resource at this timestep + robot combo
    # where the resources are greater for every box, we can prune the branch
    cache = defaultdict(list)

    def get_cache_key(robots, time_left):
        return tuple(list(robots) + [time_left])

    def update_cache_and_prune_branch(resources, robots, time_left):
        prune = False
        state_key = get_cache_key(robots, time_left)
        for resources_other in cache[state_key]:
            resources_list_updated = []
            if (resources_other > resources).any():
                resources_list_updated.append(resources_other)
            prune = prune or (resources_other >= resources).all()
            cache[state_key] = resources_list_updated

        if not prune:
            cache[state_key].append(resources)
        return prune

    best_geodes = 0
    last_time = 0
    frontier = Deque([(starting_resources, starting_robots, 0)])
    while len(frontier) > 0:
        resources, robots, time = frontier.popleft()

        ## HACK: Evilest of heuristic
        if time > last_time and max_frontier_length is not None :
            last_time = time 
            frontier = Deque(sorted(frontier, key=lambda ele: ele[0][-1], reverse=True)[:max_frontier_length])

        best_geodes = max(best_geodes, resources[-1])

        # First clean the resources associated with the state
        # And then prune the branch if applicable
        if update_cache_and_prune_branch(resources, robots, time):
            continue

        if time >= time_max:
            continue 

        build_possibilities = get_build_possibilities(
            resources, 
            costs, 
            robots,
            time_max - time + 1,
        )

        # print(
        #     f"time={time}", 
        #     f"resources={resources}", 
        #     f"robots={robots}", 
        #     build_possibilities,
        #     len(frontier), 
        #     f"best_geodes={best_geodes}"
        # )

        resources = resources + robots
        for possibility in build_possibilities:
            new_resources = resources - (possibility.reshape([4, 1]) * costs).max(0)
            new_robots = robots + possibility
            new_state = (new_resources, new_robots, time + 1)
            frontier.append(new_state)

    return best_geodes

if __name__ == "__main__":
    blueprints = read_stuff(INPUT_FILE)
    # part 1
    p1_ans = 0
    for i, blueprint in enumerate(blueprints):
        print(f"P1: {i + 1} / {len(blueprints)}")
        max_geodes = p1_search(blueprint)
        p1_ans += (i + 1) * max_geodes
    print(p1_ans)

    # part 2
    p2_ans = 1
    for i, blueprint in enumerate(blueprints[:3]):
        print(f"P2: {i + 1} / 3")
        max_geodes = p1_search(blueprint, time_max=32, max_frontier_length=100000)
        p2_ans *= max_geodes
    print(p2_ans)
