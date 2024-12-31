import re
from itertools import permutations
from functools import cache

def part01(input):
    return sum([complexity(code) for code in input.split("\n")])

def complexity(code):
    initial_sequence_from_numpad = get_best_sequence(code, numpad)
    directional_sequence = get_best_sequence(get_best_sequence(initial_sequence_from_numpad, directional), directional)
    
    min_sequence_len = len(directional_sequence)
    [numeric_part] = [int(n) for n in re.findall(r"\d+", code)]
    return numeric_part * min_sequence_len

def get_best_sequence(code, keypad):
    sequence = []
    current_key = 'A'

    for next_key in code:
        sequence = sequence + get_best_move(keypad.values(), keypad[current_key], keypad[next_key])
        current_key = next_key

    return sequence

@cache
def get_best_move(positions, start, end):
    x = end[0] - start[0]
    y = end[1] - start[1]
    move = []
    for _ in range(abs(x)):
        if (x < 0): move.append('<')
        else: move.append('>')
    for _ in range(abs(y)):
        if (y < 0): move.append('^')
        else: move.append('v')
    
    best_move = None
    if (is_valid_move(move, positions, start, end)): best_move = move
    else: best_move = list(reversed(move))

    return best_move + ['A']

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

def test_get_all_valid_permutations():
    result = get_best_move(
        numpad.values(),
        numpad['0'],
        numpad['7']
    )
    assert 3 == len(result)
    assert tuple('^^^<A') in result
    assert tuple('^^<^A') in result
    assert tuple('^<^^A') in result

def test_find_sequences_numeric():
    result = get_best_sequence('029A', numpad)
    assert 3 == len(result)
    assert tuple('<A^A>^^AvvvA') in result
    assert tuple('<A^A^>^AvvvA') in result
    assert tuple('<A^A^^>AvvvA') in result

def test_find_sequences_directional():
    result = get_best_sequence('<A^A>^^AvvvA', directional)
    assert tuple('v<<A>>^A<A>AvA<^AA>A<vAAA>^A') in result

def test_complexity():
    assert 68 * 29 == complexity("029A")

def test_part01_sample():
    assert 126384 == part01(sample)

def test_part01_input():
    with open("src/inputs/day21.txt", "r") as f:
        assert 176650 == part01(f.read())