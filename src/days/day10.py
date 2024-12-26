from collections import defaultdict

def part01(input):
    heights = defaultdict(lambda:-1)
    lines = input.split("\n")
    for y, line in enumerate(lines):
        for x, height in enumerate(line):
            heights[(x, y)] = int(height)
    
    reachable_nines = {}
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if ((x, y) in reachable_nines): continue
            calculate_reachable_nines((x, y), heights, reachable_nines)
    
    total = 0
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if (heights[(x, y)] == 0):
                total += len(reachable_nines[(x, y)])

    return total

def calculate_reachable_nines(start, heights, reachable_nines):
    current_height = heights[start]
    if (current_height == 9):
        reachable_nines[start] = set([start])
        return

    neighbours = []
    x, y = start
    if (heights[(x + 1, y)] == current_height + 1): neighbours.append((x + 1, y))
    if (heights[(x - 1, y)] == current_height + 1): neighbours.append((x - 1, y))
    if (heights[(x, y + 1)] == current_height + 1): neighbours.append((x, y + 1))
    if (heights[(x, y - 1)] == current_height + 1): neighbours.append((x, y - 1))
    
    current_reachable_nines = set()
    for neighbour in neighbours:
        if (neighbour not in reachable_nines): calculate_reachable_nines(neighbour, heights, reachable_nines)
        current_reachable_nines.update(reachable_nines[neighbour])
    
    reachable_nines[start] = current_reachable_nines


#TESTS

sample = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

def test_part01_sample():
    assert 36 == part01(sample)

def test_part01_input():
    with open("src/inputs/day10.txt", "r") as f:
        assert 719 == part01(f.read())