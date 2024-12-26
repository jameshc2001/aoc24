from collections import defaultdict

def part01(input):
    heights = get_initial_parameters(input)
    reachable_nines = {}
    for pos in list(heights.keys()):
        if (pos in reachable_nines): continue
        calculate_reachable_nines_part01(pos, heights, reachable_nines)

    return sum([len(reachable_nines[a]) for a in reachable_nines if heights[a] == 0])

def calculate_reachable_nines_part01(start, heights, reachable_nines):
    current_height = heights[start]
    if (current_height == 9):
        reachable_nines[start] = set([start])
        return

    current_reachable_nines = set()
    for neighbour in get_neighbours(start, heights, current_height):
        if (neighbour not in reachable_nines): calculate_reachable_nines_part01(neighbour, heights, reachable_nines)
        current_reachable_nines.update(reachable_nines[neighbour])
    
    reachable_nines[start] = current_reachable_nines

def part02(input):
    heights = get_initial_parameters(input)
    reachable_nines = {}
    for pos in list(heights.keys()):
        if (pos in reachable_nines): continue
        calculate_reachable_nines_part02(pos, heights, reachable_nines)
    
    return sum([reachable_nines[a] for a in reachable_nines if heights[a] == 0])

def calculate_reachable_nines_part02(start, heights, reachable_nines):
    current_height = heights[start]
    if (current_height == 9):
        reachable_nines[start] = 1
        return

    current_reachable_nines = 0
    for neighbour in get_neighbours(start, heights, current_height):
        if (neighbour not in reachable_nines): calculate_reachable_nines_part02(neighbour, heights, reachable_nines)
        current_reachable_nines += reachable_nines[neighbour]
    
    reachable_nines[start] = current_reachable_nines

def get_neighbours(start, heights, current_height):
    neighbours = []
    x, y = start
    if (heights[(x + 1, y)] == current_height + 1): neighbours.append((x + 1, y))
    if (heights[(x - 1, y)] == current_height + 1): neighbours.append((x - 1, y))
    if (heights[(x, y + 1)] == current_height + 1): neighbours.append((x, y + 1))
    if (heights[(x, y - 1)] == current_height + 1): neighbours.append((x, y - 1))
    return neighbours

def get_initial_parameters(input):
    heights = defaultdict(lambda:-1)
    lines = input.split("\n")
    for y, line in enumerate(lines):
        for x, height in enumerate(line):
            heights[(x, y)] = int(height)
    return heights

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

def test_part02_sample():
    assert 81 == part02(sample)

def test_part02_input():
    with open("src/inputs/day10.txt", "r") as f:
        assert 1530 == part02(f.read())