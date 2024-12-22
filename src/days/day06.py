import numpy as np

def part01(input):
    grid = create_grid(input)
    max_x = grid.shape[1]
    max_y = grid.shape[0]

    start_coords = np.where(grid == '^')
    gx = start_coords[1][0]
    gy = start_coords[0][0]
    dx = 0
    dy = -1

    visited = {(gx, gy)}
    grid[gy, gx] = '0'

    next_x = gx + dx
    next_y = gy + dy
    while (0 <= next_x < max_x and 0 <= next_y < max_y):
        if (grid[next_y, next_x] == '#'):
            if (dy == -1): dy = 0; dx = 1
            elif (dy == 1): dy = 0; dx = -1
            elif (dx == -1): dy = -1; dx = 0
            elif (dx == 1): dy = 1; dx = 0

            next_x = gx + dx
            next_y = gy + dy
        
        gx = gx + dx
        gy = gy + dy
        if (not (0 <= gx < max_x and 0 <= gy < max_y)): break
        grid[gy, gx] = '0'
        visited.add((gx, gy))

        next_x = gx + dx
        next_y = gy + dy
    
    print(grid)

    return len(visited)

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