import numpy as np
import cProfile
import line_profiler
import os

def part01(input):
    grid, max_y, max_x, guard, direction = initial_parameters(input)
    return len(get_path(grid, max_y, max_x, guard, direction))

def part02(input):
    grid, max_y, max_x, guard, direction = initial_parameters(input)
    new_obstacle_positions = get_path(grid, max_y, max_x, guard, direction)
    new_obstacle_positions.remove(guard)

    total = 0
    for position in new_obstacle_positions:
        new_grid = np.array(grid)
        new_grid[position[1], position[0]] = '#'
        if (has_loop(new_grid, max_y, max_x, guard, direction)): total += 1

    return total

@line_profiler.profile
def has_loop(grid, max_y, max_x, guard, direction):
    path = {tuple([tuple(guard), direction])}
    while (True):
        next = np.add(guard, direction)
        while(in_grid(max_y, max_x, next) and grid[next[1], next[0]] == '#'):
            direction = rotate_90_degrees(direction)
            next = np.add(guard, direction)
        
        guard = tuple(next)
        if (tuple([guard, direction]) in path): return True
        if (not in_grid(max_y, max_x, guard)): break
        path.add(tuple([guard, direction]))
    return False


def initial_parameters(input):
    grid = create_grid(input)
    max_y, max_x = grid.shape
    start_coords = np.where(grid == '^')
    guard = (start_coords[1][0], start_coords[0][0])
    direction = (0, -1)
    return grid,max_y,max_x,guard,direction

def get_path(grid, max_y, max_x, guard, direction):
    visited = {tuple(guard)}
    while (True):
        next = np.add(guard, direction)
        while(in_grid(max_y, max_x, next) and grid[next[1], next[0]] == '#'):
            direction = rotate_90_degrees(direction)
            next = np.add(guard, direction)
        
        guard = next
        if (not in_grid(max_y, max_x, guard)): break
        visited.add(tuple(guard))
    return visited

def rotate_90_degrees(direction):
    match (direction):
        case (0, -1): return (1, 0)
        case (0, 1): return (-1, 0)
        case (-1, 0): return (0, -1)
        case (1, 0): return (0, 1)

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

def test_part02_sample():
    assert 6 == part02(sample)

def test_part02_input():
    with open("src/inputs/day06.txt", "r") as f:
        assert 1604 == part02(f.read())

#This runs much slower than expected. I think I'm going to avoid numpy for future days and keep the elements of my sets simple.