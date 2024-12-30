import sys
import heapq as hq

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
        for cheat_destination in get_adjacent(current_pos, 2):
            if (cheat_destination not in positions): continue
            time_saved = dist[current_pos] - dist[cheat_destination] - 2
            if (time_saved >= picos_to_save): cheats += 1

        current_pos = prev[current_pos]
    assert current_pos == end

    return cheats

#this is overkill and unnecessary
def dijkstra(positions, start):
    dist = {}
    prev = {}
    Q = []
    removed = set()
    dist[start] = 0
    for pos in positions:
        if (pos != start): dist[pos] = sys.maxsize
        hq.heappush(Q, (dist[pos], pos))

    while (len(Q) > 0):
        popped = hq.heappop(Q)
        if (popped in removed): continue
        u = popped[1]

        for v in get_adjacent(u):
            if (v not in positions): continue
            alt = dist[u] + 1
            if (alt < dist[v]):
                removed.add((dist[v], v))
                dist[v] = alt
                prev[v] = u
                hq.heappush(Q, (dist[v], v))
    
    return dist, prev

def get_adjacent(pos, offset=1): return [
    (pos[0] + offset, pos[1]),
    (pos[0], pos[1] + offset),
    (pos[0] - offset, pos[1]),
    (pos[0], pos[1] - offset),
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

def test_part01_input():
    with open("src/inputs/day20.txt", "r") as f:
        assert 1323 == part01(f.read(), 100)