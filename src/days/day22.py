def part01(input):
    return sum([secret_number(int(n), 2000) for n in input.split("\n")])

def secret_number(start, iterations):
    num = start
    for _ in range(iterations):
        num = mix_then_prune(num, num * 64)
        num = mix_then_prune(num, num // 32)
        num = mix_then_prune(num, num * 2048)
    return num

def mix_then_prune(a, b): return (a ^ b) % 16777216

#TESTS

sample = """1
10
100
2024"""

def test_part01_sample():
    assert 37327623 == part01(sample)

def test_part01_input():
    with open("src/inputs/day22.txt", "r") as f:
        assert 16999668565 == part01(f.read())