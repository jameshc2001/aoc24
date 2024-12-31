import sys
from itertools import permutations

def part01(input):
    return -1

def shortest_sequences_numeric(code):
    sequences = set(get_all_valid_permutations(numpad.values(), numpad['A'], numpad[code[0]]))
    current_key = code[0]

    for next_key in code[1:]:
        new_sequences = set()
        all_valid_permutations = get_all_valid_permutations(numpad.values(), numpad[current_key], numpad[next_key])

        for s in sequences:
            for p in all_valid_permutations:
                new_sequences.add(s + p)

        sequences = new_sequences
        current_key = next_key

    return sequences


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

#TESTS

sample = """"""

# def test_part01_sample():
#     assert 1 == part01(sample)

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
    result = shortest_sequences_numeric('029A')
    assert 3 == len(result)
    assert tuple('<A^A>^^AvvvA') in result
    assert tuple('<A^A^>^AvvvA') in result
    assert tuple('<A^A^^>AvvvA') in result