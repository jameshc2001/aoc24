import numpy as np

def part01(input):
    grid = create_grid(input)
    max_y, max_x = grid.shape

    start_coords = np.where(grid == '^')
    guard = (start_coords[1][0], start_coords[0][0])
    direction = (0, -1)
    visited = {tuple(guard)}
    grid[guard[1], guard[0]] = '0'
    
    while (True):
        next = np.add(guard, direction)
        while(in_grid(max_y, max_x, next) and grid[next[1], next[0]] == '#'):
            direction = rotate_90_degrees(direction)
            next = np.add(guard, direction)
        
        guard = np.add(guard, direction)
        if (not in_grid(max_y, max_x, guard)): break
        grid[guard[1], guard[0]] = '0'
        visited.add(tuple(guard))

    return len(visited)

def rotate_90_degrees(direction):
    if (direction == (0, -1)): return (1, 0)
    elif (direction == (0, 1)): return (-1, 0)
    elif (direction == (-1, 0)): return (0, -1)
    elif (direction == (1, 0)): return (0, 1)
    return direction

def in_grid(max_y, max_x, position):
    return 0 <= position[0] < max_x and 0 <= position[1] < max_y

def create_grid(input):
    lines = input.split("\n")
    rows = len(lines)
    cols = len(lines[0])
    grid = np.full((cols, rows), '', dtype=str)

    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            grid[y, x] = character

    return grid

#TESTS

sample = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

def test_part01_sample():
    assert 41 == part01(sample)

def test_part01_input():
    with open("src/inputs/day06.txt", "r") as f:
        assert 4559 == part01(f.read())