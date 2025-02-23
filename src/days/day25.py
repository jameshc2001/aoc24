
def part01(input):
    schematics = input.split("\n\n")
    locks = list()
    keys = list()
    for schematic in schematics:
        heights = [-1, -1, -1, -1, -1]
        for y, line in enumerate(schematic.split("\n")):
            for x, value in enumerate(line):
                if (value == "#"): heights[x] = heights[x] + 1
        if (schematic[0] == "#"): locks.append(heights)
        else: keys.append(heights)
        

    total_pairs = 0
    for key in keys:
        for lock in locks:
            sum = [key[0] + lock[0], key[1] + lock[1], key[2] + lock[2], key[3] + lock[3], key[4] + lock[4]]
            if (sum[0] <= 5 and sum[1] <= 5 and sum[2] <= 5 and sum[3] <= 5 and sum[4] <= 5): total_pairs += 1

    return total_pairs

#No part02, you just need all the previous stars

#TESTS

sample = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

def test_part01_sample():
    assert 3 == part01(sample)

def test_part01_input():
    with open("src/inputs/day25.txt", "r") as f:
        assert 2691 == part01(f.read())