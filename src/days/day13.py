import re

def part01(input):
    tokens = 0
    for machine_text in input.split("\n\n"):
        lines = machine_text.split("\n")
        tokens += min_tokens(
            coords_for_line(lines[0]),
            coords_for_line(lines[1]),
            coords_for_line(lines[2])
        )
    return tokens

def coords_for_line(line):
    numbers = re.findall(r"\d+", line)
    return (int(numbers[0]), int(numbers[1]))

def min_tokens(a, b, p):
    for B in reversed(range(100)):
        A = (p[0] - (B * b[0])) / a[0]
        if (not is_whole(A, 0.0000000001)): continue
        if ((int(A) * a[0] + B * b[0]) != p[0]): continue
        if ((int(A) * a[1] + B * b[1]) != p[1]): continue
        return (int(A) * 3) + B
    return 0

def tokens_for_prize(a, b, p):
    b_pushes = (p[1] - ((a[1] * p[0]) / a[0])) / (b[1] - ((a[1] * b[0]) / a[0]))
    a_pushes = (p[0] - (b_pushes * b[0])) / a[0]

    deviation = 0.0000000001
    if (a_pushes < 0 or b_pushes < 0 or not is_whole(a_pushes, deviation) or not is_whole(b_pushes, deviation)): return 0
    else: return (int(a_pushes) * 3) + int(b_pushes)

def is_whole(value, deviation):
    rounded = round(value)
    d = abs(deviation)
    return rounded - d <= value <= rounded + d

#TESTS

sample = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

def test_part01_sample():
    assert 480 == part01(sample)

def test_part01_input():
    with open("src/inputs/day13.txt", "r") as f:
        assert 36571 == part01(f.read())