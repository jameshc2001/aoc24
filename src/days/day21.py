import re
from itertools import permutations
from functools import cache

def part01(input):
    return sum([complexity(code) for code in input.split("\n")])

def complexity(code):
    initial_sequences_from_numpad = filter_optimal_sequences(all_sequences(code, numpad))

    directional_sequences = set()
    for i in initial_sequences_from_numpad:
        directional_sequences.update(all_sequences(i, directional))
    directional_sequences = filter_optimal_sequences(directional_sequences)
    
    min_sequence_len = length_of_directional_sequence(directional_sequences.pop())
    [numeric_part] = [int(n) for n in re.findall(r"\d+", code)]
    return numeric_part * min_sequence_len

def shortest_sequences_numeric(code):
    return filter_optimal_sequences(all_sequences(code, numpad))

def shortest_sequences_directional(code):
    return filter_optimal_sequences(all_sequences(code, directional))

def filter_optimal_sequences(sequences):
    min_length = length_of_directional_sequence(min(sequences, key=lambda s: length_of_directional_sequence(s)))
    return [s for s in sequences if length_of_directional_sequence(s) == min_length]

@cache
def length_of_directional_sequence(sequence):
    length = 0
    current_key = 'A'
    for next_key in sequence:
        current_x, current_y = directional[current_key]
        next_x, next_y = directional[next_key]
        length += abs(next_x - current_x) + abs(next_y - current_y) + 1 #additional 1 is for 'A'
        current_key = next_key
    return length

def all_sequences(code, keypad):
    sequences = set(get_all_valid_permutations(keypad.values(), keypad['A'], keypad[code[0]]))
    current_key = code[0]

    for next_key in code[1:]:
        new_sequences = set()
        all_valid_permutations = get_all_valid_permutations(keypad.values(), keypad[current_key], keypad[next_key])

        for s in sequences:
            for p in all_valid_permutations:
                new_sequences.add(s + p)

        sequences = new_sequences
        current_key = next_key

    return sequences

@cache
def get_all_valid_permutations(positions, start, end):
    x = end[0] - start[0]
    y = end[1] - start[1]
    moves = []
    for _ in range(abs(x)):
        if (x < 0): moves.append('<')
        else: moves.append('>')
    for _ in range(abs(y)):
        if (y < 0): moves.append('^')
        else: moves.append('v')
    
    all_permutations = set(permutations(moves, len(moves)))
    return [p + tuple('A') for p in all_permutations if is_valid_permutation(p, positions, start, end)]

def is_valid_permutation(permutation, positions, start, end):
    x, y = start
    for move in permutation:
        if (move == '>'): x += 1
        elif (move == 'v'): y += 1
        elif (move == '<'): x -= 1
        elif (move == '^'): y -= 1
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

def test_get_all_permutations():
    result = get_all_valid_permutations(
        numpad.values(),
        numpad['0'],
        numpad['7']
    )
    assert 3 == len(result)
    assert tuple('^^^<A') in result
    assert tuple('^^<^A') in result
    assert tuple('^<^^A') in result

def test_shortest_sequences_numeric():
    result = all_sequences('029A', numpad)
    assert 3 == len(result)
    assert tuple('<A^A>^^AvvvA') in result
    assert tuple('<A^A^>^AvvvA') in result
    assert tuple('<A^A^^>AvvvA') in result

def test_shortest_sequences_directional():
    result = all_sequences('<A^A>^^AvvvA', directional)
    assert tuple('v<<A>>^A<A>AvA<^AA>A<vAAA>^A') in result

def test_complexity():
    assert 68 * 29 == complexity("029A")

def test_part01_sample():
    assert 126384 == part01(sample)

def test_part01_input():
    with open("src/inputs/day21.txt", "r") as f:
        assert 176650 == part01(f.read())