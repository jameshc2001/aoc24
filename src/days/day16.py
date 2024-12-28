import sys

def part01(input):
    walls = set()
    start = (-1, -1)
    end = (-1, -1)
    direction = (1, 0)
    for y, line in enumerate(input.split("\n")):
        for x, character in enumerate(line):
            if (character == '#'): walls.add((x, y))
            elif (character == 'S'): start = (x, y)
            elif (character == 'E'): end = (x, y)

    return search(start, direction, walls, end, set(), 0)

def search(pos, direction, walls, end, path, cost):
    if (pos == end): return cost
    if (pos in walls or pos in path): return sys.maxsize

    path.add(pos)
    clockwise = rotate_clockwise(direction)
    counter_clockwise = rotate_counter_clockwise(direction)
    return min(
        search(add_direction(pos, direction), direction, walls, end, path.copy(), cost + 1),
        search(add_direction(pos, clockwise), clockwise, walls, end, path.copy(), cost + 1001),
        search(add_direction(pos, counter_clockwise), counter_clockwise, walls, end, path.copy(), cost + 1001)
    )

def add_direction(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])

def rotate_counter_clockwise(direction):
    new_direction = rotate_clockwise(direction)
    return (-new_direction[0], -new_direction[1])

def rotate_clockwise(direction):
    if (direction == (1, 0)): return (0, 1)
    if (direction == (0, 1)): return (-1, 0)
    if (direction == (-1, 0)): return (0, -1)
    if (direction == (0, -1)): return (1, 0)


#TESTS

sample = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

def test_part01_sample():
    assert 11048 == part01(sample)

def test_part01_input():
    with open("src/inputs/day16.txt", "r") as f:
        sys.setrecursionlimit(10000)
        assert 1412971 == part01(f.read())