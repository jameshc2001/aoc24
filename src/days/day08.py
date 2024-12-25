from collections import defaultdict
from itertools import combinations

def part01(input):
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

    antinodes = set()
    for _, group in grouped_antennas.items():
        for a, b in list(combinations(group, 2)):
            aToB = (b[0] - a[0], b[1] - a[1])
            antinodes.add((a[0] - aToB[0], a[1] - aToB[1]))
            antinodes.add((b[0] + aToB[0], b[1] + aToB[1]))

    return len([a for a in antinodes if 0 <= a[0] < max_x and 0 <= a[1] < max_y])

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