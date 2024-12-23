import collections

def part01(input):
    left, right = get_left_and_right(input)
    left.sort()
    right.sort()
    zipped = list(zip(left, right))
    return sum(abs(pair[0] - pair[1]) for pair in zipped)

def part02(input):
    left, right = get_left_and_right(input)
    right_occurrences = collections.Counter(right)
    return sum(l * right_occurrences[l] for l in left)

def get_left_and_right(input):
    left = []
    right = []
    for line in input.split("\n"):
        l, r = line.split("   ")
        left.append(int(l))
        right.append(int(r))
    return left,right

#TESTS

sample = """3   4
4   3
2   5
1   3
3   9
3   3"""

def test_part01_sample():
    assert 11 == part01(sample)

def test_part01_input():
    with open("src/inputs/day01.txt", "r") as f:
        assert 1765812 == part01(f.read())

def test_part02_sample():
    assert 31 == part02(sample)

def test_part02_input():
    with open("src/inputs/day01.txt", "r") as f:
        assert 20520794 == part02(f.read())
