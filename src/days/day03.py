import re

def part01(input):
    instructions = re.findall(r"mul\(\d+,\d+\)", input)
    return sum(execute_mul_instruction(instruction) for instruction in instructions)

def execute_mul_instruction(instruction):
    numbers = re.findall("\d+", instruction)
    return int(numbers[0]) * int(numbers[1])

def part02(input):
    instructions = re.findall(r"(?:mul\(\d+,\d+\))|(?:do\(\))|(?:don't\(\))", input)
    multiplication_enabled = True
    total = 0

    for instruction in instructions:
        if ("mul" in instruction and multiplication_enabled): total += execute_mul_instruction(instruction)
        elif ("don\'t()" in instruction): multiplication_enabled = False
        elif ("do()" in instruction): multiplication_enabled = True

    return total

#TESTS

def test_part01_sample():
    sample = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    assert 161 == part01(sample)

def test_part01_input():
    with open("src/inputs/day03.txt", "r") as f:
        assert 173731097 == part01(f.read())

def test_part02_sample():
    sample = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    assert 48 == part02(sample)

def test_part02_input():
    with open("src/inputs/day03.txt", "r") as f:
        assert 93729253 == part02(f.read())