import sys

def part01(input, picos_to_save):

    start = None
    end = None
    positions = set()
    for y, line in enumerate(input.split("\n")):
        for x, character in enumerate(line):
            if (character != '#'): positions.add((x, y))
            if (character == 'S'): start = (x, y)
            if (character == 'E'): end = (x, y)
    
    dist, prev = dijkstra(positions, end)

    cheats = 0
    current_pos = start
    while (current_pos in prev):
        #TODO: fancy cheat checking code here

        current_pos = prev[current_pos]
    assert current_pos == end

    return cheats

def dijkstra(positions, start):
    dist = {}
    prev = {}
    Q = set()
    for pos in positions:
        dist[pos] = sys.maxsize
        Q.add(pos)
    dist[start] = 0

    while (len(Q) > 0):
        u = min(Q, key=lambda pos: dist[pos])
        Q.remove(u)

        for v in get_adjacent(u):
            if (v not in positions): continue
            alt = dist[u] + 1
            if (alt < dist[v]):
                dist[v] = alt
                prev[v] = u
    
    return dist, prev


def get_adjacent(pos): return [
    (pos[0] + 1, pos[1]),
    (pos[0], pos[1] + 1),
    (pos[0] - 1, pos[1]),
    (pos[0], pos[1] - 1),
]


#TESTS

sample = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

def test_part01_sample():
    assert 8 == part01(sample, 12)