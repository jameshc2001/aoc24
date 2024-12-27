import re
from collections import defaultdict

class Robot:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def move(self, max_x, max_y):
        new_x = (self.pos[0] + self.vel[0]) % max_x
        new_y = (self.pos[1] + self.vel[1]) % max_y
        return Robot((new_x, new_y), self.vel)


def part01(input, max_x, max_y):
    robots = get_robots(input)
    for _ in range(100):
        robots = [robot.move(max_x, max_y) for robot in robots]
    
    mid_x = max_x // 2
    mid_y = max_y // 2
    top_left, top_right, bottom_left, bottom_right = 0, 0, 0, 0
    for robot in robots:
        if (robot.pos[0] < mid_x):
            if (robot.pos[1] < mid_y): top_left += 1
            elif (robot.pos[1] > mid_y): bottom_left += 1
        elif(robot.pos[0] > mid_x):
            if (robot.pos[1] < mid_y): top_right += 1
            elif (robot.pos[1] > mid_y): bottom_right += 1

    return top_left * top_right * bottom_left * bottom_right

def part02(input, max_x, max_y):
    robots = get_robots(input)
    min_groups = max_x * max_y
    tree_second = -1
    for second in range(1, 10000):
        robots = [robot.move(max_x, max_y) for robot in robots]
        xs = set()
        ys = set()
        for robot in robots:
            xs.add(robot.pos[0])
            ys.add(robot.pos[1])
        groups = len(xs) + len(ys)
        if (groups < min_groups):
            # print_robots(robots, max_x, max_y)
            min_groups = groups
            tree_second = second

    return tree_second

def get_robots(input):
    robots = []
    for line in input.split("\n"):
        nums = [int(n) for n in re.findall(r"-?\d+", line)]
        robots.append(Robot((nums[0], nums[1]), (nums[2], nums[3])))
    return robots

def print_robots(robots, max_x, max_y):
    pos_to_num_of_robots = defaultdict(lambda:0)
    for robot in robots:
        pos_to_num_of_robots[robot.pos] += 1
    pos_to_num_of_robots = dict(pos_to_num_of_robots)

    output = "\n"
    for y in range(max_y):
        for x in range(max_x):
            if ((x, y) in pos_to_num_of_robots): output += str(pos_to_num_of_robots[(x, y)])
            else: output += "."
        output += "\n"
    print(output)


#TESTS

sample = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

def test_part01_sample():
    assert 12 == part01(sample, 11, 7)

def test_part01_input():
    with open("src/inputs/day14.txt", "r") as f:
        assert 214109808 == part01(f.read(), 101, 103)

def test_part02_input():
    with open("src/inputs/day14.txt", "r") as f:
        assert 7687 == part02(f.read(), 101, 103)