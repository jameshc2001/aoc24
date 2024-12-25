import re

def part01(input):
    equations_text = [re.findall(r"\d+", equation) for equation in input.split("\n")]
    equations = [[int(number) for number in equation] for equation in equations_text]
    return sum([equation[0] for equation in equations if is_valid_part01(equation)])

def is_valid_part01(equation):
    return is_valid_recursive_part01(equation[0], 0, equation[1:])

def is_valid_recursive_part01(goal, total, numbers):
    if (len(numbers) == 0): return goal == total
    if (is_valid_recursive_part01(goal, total + numbers[0], numbers[1:])): return True
    elif (is_valid_recursive_part01(goal, total * numbers[0], numbers[1:])): return True
    else: return False

def part02(input):
    equations_text = [re.findall(r"\d+", equation) for equation in input.split("\n")]
    equations = [[int(number) for number in equation] for equation in equations_text]
    return sum([equation[0] for equation in equations if is_valid_part02(equation)])

def is_valid_part02(equation):
    return is_valid_recursive_part02(equation[0], 0, equation[1:])

def is_valid_recursive_part02(goal, total, numbers):
    if (total > goal): return False
    if (len(numbers) == 0): return goal == total
    if (is_valid_recursive_part02(goal, total + numbers[0], numbers[1:])): return True
    elif (is_valid_recursive_part02(goal, total * numbers[0], numbers[1:])): return True
    elif (is_valid_recursive_part02(goal, concatenate(total, numbers[0]), numbers[1:])): return True
    else: return False

def concatenate(a, b): return int(str(a) + str(b))

#TESTS

sample = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

def test_part01_sample():
    assert 3749 == part01(sample)

def test_part01_input():
    with open("src/inputs/day07.txt", "r") as f:
        assert 8401132154762 == part01(f.read())

def test_part02_sample():
    assert 11387 == part02(sample)

def test_part02_input():
    with open("src/inputs/day07.txt", "r") as f:
        assert 95297119227552 == part02(f.read())