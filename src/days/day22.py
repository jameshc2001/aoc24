from collections import defaultdict

def part01(input):
    return sum([secret_number(int(n), 2000) for n in input.split("\n")])

def secret_number(start, iterations):
    num = start
    for _ in range(iterations):
        num = get_next_secret_number(num)
    return num

def part02(input):
    starting_numbers = [int(n) for n in input.split("\n")]
    monkey_business = defaultdict(lambda:0) #change tuples to running totals

    for nums in starting_numbers:
        generate_monkey_business(nums, monkey_business)

    return max(monkey_business.values())

def generate_monkey_business(start, monkey_business):
    encountered_tuples = set()
    changes = []
    current = start
    prev_digit = int(str(current)[-1])
    for i in range(2000):
        current = get_next_secret_number(current)
        current_digit = int(str(current)[-1])
        changes.append(current_digit - prev_digit)

        if (i >= 3):
            change_tuple = tuple(changes)
            if (change_tuple not in encountered_tuples):
                monkey_business[change_tuple] += current_digit
                encountered_tuples.add(change_tuple)
            changes.pop(0)

        prev_digit = current_digit

def get_next_secret_number(num):
    num = mix_then_prune(num, num * 64)
    num = mix_then_prune(num, num // 32)
    num = mix_then_prune(num, num * 2048)
    return num

def mix_then_prune(a, b): return (a ^ b) % 16777216

#TESTS

def test_part01_sample():
    sample = """1
10
100
2024"""
    assert 37327623 == part01(sample)

def test_part01_input():
    with open("src/inputs/day22.txt", "r") as f:
        assert 16999668565 == part01(f.read())

def test_part02_sample():
    sample = """1
2
3
2024"""
    assert 23 == part02(sample)

def test_part02_input():
    with open("src/inputs/day22.txt", "r") as f:
        assert 1898 == part02(f.read())