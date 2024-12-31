import re
import sys
from functools import cache
from itertools import pairwise

def solution(input, iterations):
    return sum([complexity(code, iterations) for code in input.split("\n")])

def complexity(code, iterations):
    sequence = get_best_sequence(code, numpad)

    length = 0
    for a, b in pairwise(['A'] + sequence):
        length += get_human_instructions(a, b, iterations)

    [numeric_part] = [int(n) for n in re.findall(r"\d+", code)]
    return numeric_part * length

@cache
def get_human_instructions(current_key, next_key, depth):
    if (depth == 0): return 1

    valid_moves = get_valid_moves(directional.values(), directional[current_key], directional[next_key])

    minimum = sys.maxsize
    for move in valid_moves:
        total = 0
        for a, b in pairwise(['A'] + move):
            total += get_human_instructions(a, b, depth - 1)
        if (total < minimum): minimum = total

    return minimum

def get_best_sequence(code, keypad):
    sequence = []
    current_key = 'A'

    for next_key in code:
        sequence.extend(get_best_move(keypad.values(), keypad[current_key], keypad[next_key]))
        current_key = next_key

    return sequence

def get_best_move(positions, start, end):
    if (start == end): return ['A']

    valid_moves = get_valid_moves(positions, start, end)

    for m in valid_moves:
        if (m[-2] == '^'): return m
    for m in valid_moves:
        if (m[-2] == '>'): return m
    for m in valid_moves:
        if (m[-2] == 'v'): return m

    return valid_moves[0]

def get_valid_moves(positions, start, end):
    x = end[0] - start[0]
    y = end[1] - start[1]
    move = []
    for _ in range(abs(x)):
        if (x < 0): move.append('<')
        else: move.append('>')
    for _ in range(abs(y)):
        if (y < 0): move.append('^')
        else: move.append('v')

    moves = [move, list(reversed(move))]
    valid_moves = [m + ['A'] for m in moves if is_valid_move(m, positions, start, end)]

    if (len(valid_moves) == 0):
        print('fudge')

    return valid_moves

def is_valid_move(move, positions, start, end):
    x, y = start
    for key in move:
        if (key == '>'): x += 1
        elif (key == 'v'): y += 1
        elif (key == '<'): x -= 1
        elif (key == '^'): y -= 1
        if ((x, y) not in positions): return False
    return (x, y) == end

numpad = {
    '7': (0, 0), '8': (1, 0), '9': (2, 0),
    '4': (0, 1), '5': (1, 1), '6': (2, 1),
    '1': (0, 2), '2': (1, 2), '3': (2, 2),
                 '0': (1, 3), 'A': (2, 3)
}

directional = {
                 '^': (1, 0), 'A': (2, 0),
    '<': (0, 1), 'v': (1, 1), '>': (2, 1)
}

#TESTS

sample = """029A
980A
179A
456A
379A"""

def test_complexity():
    assert 68 * 29 == complexity("029A", 2)

def test_part01_sample():
    assert 126384 == solution(sample, 2)

def test_part01_input():
    with open("src/inputs/day21.txt", "r") as f:
        assert 176650 == solution(f.read(), 2)

def test_part02_input():
    with open("src/inputs/day21.txt", "r") as f:
        assert 218160099093716 == solution(f.read(), 25)