import sys

def part01(input):
    positions = set()
    start = (-1, -1)
    end = (-1, -1)
    for y, line in enumerate(input.split("\n")):
        for x, character in enumerate(line):
            if (character != '#'): positions.add((x, y)) #always add position
            if (character == 'S'): start = (x, y)
            elif (character == 'E'): end = (x, y)

    distances = dijkstra(positions, start)
    return distances[end]

def dijkstra(positions, start):
    dist = {}
    direction = {}
    prev = {}
    Q = set()
    for pos in positions:
        dist[pos] = sys.maxsize
        Q.add(pos)
    dist[start] = 0
    direction[start] = (1, 0)

    while (len(Q) > 0):
        u = min(Q, key=lambda pos: dist[pos])
        Q.remove(u)

        neighbours = [pos for pos in get_adjacents(u) if pos in Q]
        for v in neighbours:
            alt = dist[u] + 1
            dir = get_direction(u, v)
            if (dir != direction[u]): alt += 1000
            if (alt < dist[v]):
                dist[v] = alt
                prev[v] = u
                direction[v] = dir
    
    return dist #, prev, direction
        
def get_adjacents(pos): return [
    (pos[0] + 1, pos[1]),
    (pos[0], pos[1] + 1),
    (pos[0] - 1, pos[1]),
    (pos[0], pos[1] - 1),
]

def get_direction(a, b): return (b[0] - a[0], b[1] - a[1])

def add_direction(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])

def rotate_counter_clockwise(direction):
    new_direction = rotate_clockwise(direction)
    return (-new_direction[0], -new_direction[1])

def rotate_clockwise(direction):
    if (direction == (1, 0)): return (0, 1)
    if (direction == (0, 1)): return (-1, 0)
    if (direction == (-1, 0)): return (0, -1)
    if (direction == (0, -1)): return (1, 0)


#TESTS

sample = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

def test_part01_sample():
    assert 11048 == part01(sample)

def test_part01_input():
    with open("src/inputs/day16.txt", "r") as f:
        sys.setrecursionlimit(10000)
        assert 98416 == part01(f.read())