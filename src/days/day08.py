from collections import defaultdict
from itertools import combinations

def part01(input):
    max_y, max_x, grouped_antennas = get_initial_parameters(input)

    antinodes = set()
    for _, group in grouped_antennas.items():
        for a, b in list(combinations(group, 2)):
            aToB = (b[0] - a[0], b[1] - a[1])
            antinodes.add((a[0] - aToB[0], a[1] - aToB[1]))
            antinodes.add((b[0] + aToB[0], b[1] + aToB[1]))

    return len([a for a in antinodes if in_range(a, max_x, max_y)])

def part02(input):
    max_y, max_x, grouped_antennas = get_initial_parameters(input)

    antinodes = set()
    for _, group in grouped_antennas.items():
        for a, b in list(combinations(group, 2)):
            aToB = (b[0] - a[0], b[1] - a[1])
            m = 0
            while (True):
                new_a = (a[0] - m * aToB[0], a[1] - m * aToB[1])
                new_b = (b[0] + m * aToB[0], b[1] + m * aToB[1])
                if (in_range(new_a, max_x, max_y)): antinodes.add(new_a)
                if (in_range(new_b, max_x, max_y)): antinodes.add(new_b)
                if (not in_range(new_a, max_x, max_y) and not in_range(new_b, max_x, max_y)): break
                m += 1

    return len(antinodes)

def get_initial_parameters(input):
    lines = input.split("\n")
    max_y = len(lines)
    max_x = len(lines[0])
    antennas = set()
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            if (character != '.'):
                antennas.add((x, y, character))

    grouped_antennas = defaultdict(list)
    for a in antennas: grouped_antennas[a[2]].append((a[0], a[1]))
    grouped_antennas = dict(grouped_antennas)
    return max_y,max_x,grouped_antennas

def in_range(pos, max_x, max_y): return 0 <= pos[0] < max_x and 0 <= pos[1] < max_y

#TESTS

sample = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

def test_part01_sample():
    assert 14 == part01(sample)

def test_part01_input():
    with open("src/inputs/day08.txt", "r") as f:
        assert 311 == part01(f.read())

def test_part02_sample():
    assert 34 == part02(sample)

def test_part02_input():
    with open("src/inputs/day08.txt", "r") as f:
        assert 1115 == part02(f.read())