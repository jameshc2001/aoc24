import re
import sys

def part01(input, num_of_bytes, end):
    lines = input.split("\n")
    corrupted = set()
    for line_index in range(num_of_bytes):
        nums = re.findall(r"\d+", lines[line_index])
        corrupted.add((int(nums[0]), int(nums[1])))

    positions = set()
    for x in range(end + 1):
        for y in range(end + 1):
            if ((x, y) not in corrupted): positions.add((x, y))

    print_grid(positions, end)
    dist, _ = dijkstra(positions, (0, 0))
    return dist[(end, end)]

def print_grid(positions, end):
    output = "\n"
    for y in range(end + 1):
        for x in range(end + 1):
            if (x, y) in positions: output += '.'
            else: output += '#'
        output += "\n"
    print(output)

def dijkstra(positions, start):
    dist = {}
    prev = {}
    Q = set()
    for pos in positions:
        dist[pos] = sys.maxsize
        Q.add(pos)
    dist[start] = 0
    prev[start] = None
    
    while (len(Q) > 0):
        u = min(Q, key=lambda pos: dist[pos])
        Q.remove(u)

        for v in get_adjacent(u):
            if (v not in Q): continue
            alt = dist[u] + 1
            if (alt < dist[v]):
                dist[v] = alt
                prev[v] = u
    
    return dist, prev

def get_adjacent(pos): return [
    (pos[0] + 1, pos[1]),
    (pos[0], pos[1] + 1),
    (pos[0] - 1, pos[1]),
    (pos[0], pos[1] - 1)
]

#TESTS

sample = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

def test_part01_sample():
    assert 22 == part01(sample, 12, 6)

def test_part01_input():
    with open("src/inputs/day18.txt", "r") as f:
        assert 292 == part01(f.read(), 1024, 70)