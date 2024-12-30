from functools import cache

def part01(input):
    towels, patterns = input.split("\n\n")
    towels = tuple(towels.split(", "))
    patterns = patterns.split("\n")
    return len([pattern for pattern in patterns if ways_to_make_pattern(towels, pattern) > 0])

def part02(input):
    towels, patterns = get_towels_and_patterns(input)
    return sum([ways_to_make_pattern(towels, pattern) for pattern in patterns])

@cache
def ways_to_make_pattern(towels, pattern):
    if (len(pattern) == 0): return 1
    return sum([ways_to_make_pattern(towels, pattern[len(towel):]) for towel in towels if towel == pattern[:len(towel)]])

def get_towels_and_patterns(input):
    towels, patterns = input.split("\n\n")
    towels = tuple(towels.split(", "))
    patterns = patterns.split("\n")
    return towels,patterns

#TESTS

sample = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

def test_part01_sample():
    assert 6 == part01(sample)

def test_part01_input():
    with open("src/inputs/day19.txt", "r") as f:
        assert 216 == part01(f.read())

def test_part02_sample():
    assert 16 == part02(sample)

def test_part02_input():
    with open("src/inputs/day19.txt", "r") as f:
        assert 603191454138773 == part02(f.read())