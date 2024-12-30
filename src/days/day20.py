import sys
import heapq as hq

def solution(input, picos_to_save, max_cheat_time):
    start, end, positions = get_initial_parameters(input)
    dist, prev = dijkstra(positions, end)

    cheats = 0
    current_pos = start
    while (current_pos in prev):
        for cheat_destination, cheat_time in get_cheat_destinations(current_pos, positions, max_cheat_time).items():
            time_saved = dist[current_pos] - dist[cheat_destination] - cheat_time
            if (time_saved >= picos_to_save): cheats += 1
        current_pos = prev[current_pos]

    return cheats

def get_cheat_destinations(pos, positions, distance):
    destinations = {}
    for x in range(-distance - 1, distance + 1):
        for y in range(-distance - 1, distance + 1):
            dest = (pos[0] + x, pos[1] + y)
            time = manhattan_distance(pos, dest)
            if (dest in positions and time <= distance):
                destinations[dest] = time
    return destinations

def manhattan_distance(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])

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

def get_initial_parameters(input):
    start = None
    end = None
    positions = set()
    for y, line in enumerate(input.split("\n")):
        for x, character in enumerate(line):
            if (character != '#'): positions.add((x, y))
            if (character == 'S'): start = (x, y)
            if (character == 'E'): end = (x, y)
    return start,end,positions


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
    assert 8 == solution(sample, 12, 2)

def test_part01_input():
    with open("src/inputs/day20.txt", "r") as f:
        assert 1323 == solution(f.read(), 100, 2)

def test_part02_sample():
    assert 67 == solution(sample, 66, 20)

def test_part02_input():
    with open("src/inputs/day20.txt", "r") as f:
        assert 983905 == solution(f.read(), 100, 20)