import numpy as np

def part01(input):
    rows, cols, grid = create_grid(input)
    total = 0
    for x in range(cols):
        for y in range(rows):
            if (grid[x, y] != "X"): continue

            if ((get(grid, x, y) + get(grid, x + 1, y) + get(grid, x + 2, y) + get(grid, x + 3, y)) == "XMAS"): total += 1
            if ((get(grid, x, y) + get(grid, x - 1, y) + get(grid, x - 2, y) + get(grid, x - 3, y)) == "XMAS"): total += 1
            if ((get(grid, x, y) + get(grid, x, y + 1) + get(grid, x, y + 2) + get(grid, x, y + 3)) == "XMAS"): total += 1
            if ((get(grid, x, y) + get(grid, x, y - 1) + get(grid, x, y - 2) + get(grid, x, y - 3)) == "XMAS"): total += 1

            if ((get(grid, x, y) + get(grid, x + 1, y + 1) + get(grid, x + 2, y + 2) + get(grid, x + 3, y + 3)) == "XMAS"): total += 1
            if ((get(grid, x, y) + get(grid, x - 1, y - 1) + get(grid, x - 2, y - 2) + get(grid, x - 3, y - 3)) == "XMAS"): total += 1

            if ((get(grid, x, y) + get(grid, x + 1, y - 1) + get(grid, x + 2, y - 2) + get(grid, x + 3, y - 3)) == "XMAS"): total += 1
            if ((get(grid, x, y) + get(grid, x - 1, y + 1) + get(grid, x - 2, y + 2) + get(grid, x - 3, y + 3)) == "XMAS"): total += 1

    return total

def part02(input):
    rows, cols, grid = create_grid(input)
    permutations = ["SAM", "MAS"]
    total = 0
    for x in range(cols):
        for y in range(rows):
            if (grid[x, y] != "A"): continue

            a = get(grid, x - 1, y - 1) + "A" + get(grid, x + 1, y + 1)
            b = get(grid, x + 1, y - 1) + "A" + get(grid, x - 1, y + 1)

            if (a in permutations and b in permutations): total += 1
    
    return total

def create_grid(input):
    lines = input.split("\n")
    rows = len(lines)
    cols = len(lines[0])
    grid = np.full((cols, rows), '', dtype=str)

    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            grid[x, y] = character

    return rows,cols,grid

def get(grid, x, y):
    a, b = grid.shape
    if (0 <= x < a and 0 <= y < b): return grid[x, y]
    return ""
    

#TESTS

sample = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

def test_part01_sample():
    assert 18 == part01(sample)

def test_part01_input():
    with open("src/inputs/day04.txt", "r") as f:
        assert 2464 == part01(f.read())

def test_part02_sample():
    assert 9 == part02(sample)

def test_part02_input():
    with open("src/inputs/day04.txt", "r") as f:
        assert 1982 == part02(f.read())