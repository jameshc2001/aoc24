import sys
import heapq

class Vertex():
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
    
    def __hash__(self):
        return hash((self.position, self.direction))

    def __eq__(self, value):
        return self.position == value.position and self.direction == value.direction

#end can be reached from multiple directions

def part01(input):
    vertices = set()
    start_position = None
    end_position = None
    for y, line in enumerate(input.split("\n")):
        for x, character in enumerate(line):
            pos = (x, y)
            if (character != '#'):
                vertices.add(Vertex(pos, (1, 0)))
                vertices.add(Vertex(pos, (0, 1)))
                vertices.add(Vertex(pos, (-1, 0)))
                vertices.add(Vertex(pos, (0, -1)))
            if (character == 'S'): start_position = pos
            elif (character == 'E'): end_position = pos

    dist, _ = big_dijkstra(vertices, Vertex(start_position, (1, 0)))
    return min([dist[v] for v in vertices if v.position == end_position])

def big_dijkstra(vertices, start):
    dist = {}
    prev = {}
    Q = set()
    for v in vertices:
        dist[v] = sys.maxsize
        Q.add(v)
    dist[start] = 0
    prev[start] = []

    original_size = len(Q)

    while (len(Q) > 0):
        print((len(Q) / original_size) * 100)
        u = min(Q, key=lambda pos: dist[pos])
        Q.remove(u)

        for v, cost in get_neighbours_with_cost(u, Q):
            alt = dist[u] + cost
            if (alt < dist[v]):
                dist[v] = alt
                prev[v] = u
    
    return dist, prev

def get_neighbours_with_cost(u, Q):
    next = Vertex(add_direction(u.position, u.direction), u.direction)
    clockwise = Vertex(u.position, rotate_clockwise(u.direction))
    counter_clockwise = Vertex(u.position, rotate_counter_clockwise(u.direction))

    neighbours_with_cost = []
    if (next in Q): neighbours_with_cost.append((next, 1))
    if (clockwise in Q): neighbours_with_cost.append((clockwise, 1000))
    if (counter_clockwise in Q): neighbours_with_cost.append((counter_clockwise, 1000))

    return neighbours_with_cost

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

def test_part02_sample():
    assert 64 == part02(sample)