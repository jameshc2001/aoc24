import re
from itertools import permutations
from functools import cache

def solution(input, iterations):
    return sum([complexity(code, iterations) for code in input.split("\n")])

def complexity(code, iterations):
    sequence = get_best_sequence(code, numpad)
    for _ in range(iterations):
        print(len(sequence))
        sequence = get_best_sequence(sequence, directional)
    
    [numeric_part] = [int(n) for n in re.findall(r"\d+", code)]
    return numeric_part * len(sequence)

def get_best_sequence(code, keypad):
    sequence = []
    current_key = 'A'

    for next_key in code:
        sequence = sequence + get_best_move(keypad.values(), keypad[current_key], keypad[next_key])
        current_key = next_key

    return sequence

@cache
def get_best_move(positions, start, end):
    if (start == end): return ['A']

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
    valid_moves = [m for m in moves if is_valid_move(m, positions, start, end)]

    for m in valid_moves:
        if (m[-1] == '^' or m[-1] == '>'): return m + ['A']
    for m in valid_moves:
        if (m[-1] == 'v'): return m + ['A']

    return valid_moves[0] + ['A']

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
        assert 176650 == solution(f.read(), 25)