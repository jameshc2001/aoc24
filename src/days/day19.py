from functools import cache

def part01(input):
    towels, patterns = input.split("\n\n")
    towels = tuple(towels.split(", "))
    patterns = patterns.split("\n")
    return len([pattern for pattern in patterns if can_make_pattern(towels, pattern)])

@cache
def can_make_pattern(towels, pattern):
    if (len(pattern) == 0): return True

    for towel in towels:
        if (len(towel) > len(pattern)): continue
        if (towel == pattern[:len(towel)] and can_make_pattern(towels, pattern[len(towel):])): return True
        
    return False

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