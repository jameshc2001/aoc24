import unittest

def part01(input):
    lines = input.split("\n")
    reports = [[int(num) for num in line.split(" ")] for line in lines]
    return len([report for report in reports if is_safe_part01(report)])

def part02(input):
    lines = input.split("\n")
    reports = [[int(num) for num in line.split(" ")] for line in lines]
    return len([report for report in reports if is_safe_part02(report)])

def is_safe_part02(report):
    for index in range(len(report)):
        if (is_safe_part01(report[:index] + report[index+1:])): return True
    return False

def is_safe_part01(report):
    increasing = report[0] < report[1]
    for index, current in enumerate(report):
        if (index == 0): continue
        prev = report[index - 1]
        if (increasing and prev > current): return False
        if (not increasing and prev < current): return False
        diff = abs(prev - current)
        if (diff < 1 or diff > 3): return False
    return True


#TESTS

sample = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

def test_part01_sample():
    assert 2 == part01(sample)

def test_part01_input():
    with open("src/inputs/day02.txt", "r") as f:
        assert 510 == part01(f.read())

def test_part02_sample():
    assert 4 == part02(sample)

def test_part02_input():
    with open("src/inputs/day02.txt", "r") as f:
        assert 553 == part02(f.read())