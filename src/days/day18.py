import re
import sys
import heapq as hq

def part01(input, num_of_bytes, end):
    corrupted, positions = get_initial_parameters(input, end)
    return length_of_shortest_path(positions, set(corrupted[:num_of_bytes]), end)

def part02(input, start_num_of_bytes, end):
    corrupted, positions = get_initial_parameters(input, end)
    
    #binary search
    left = start_num_of_bytes
    right = len(corrupted)
    midpoint = None
    while (True):
        midpoint = left + ((right - left) // 2)
        if (left == midpoint or right == midpoint): break
        shortest = length_of_shortest_path(positions, corrupted[:midpoint], end)
        if (shortest == sys.maxsize):
            right = midpoint
        else:
            left = midpoint

    first_blocking_byte = None
    if (midpoint == left): first_blocking_byte = corrupted[right-1]
    else: first_blocking_byte = corrupted[left-1]

    return str(first_blocking_byte[0]) + "," + str(first_blocking_byte[1])

def length_of_shortest_path(positions, corrupted, end):
    dist, _ = dijkstra(positions, corrupted, (0, 0))
    return dist[(end, end)]

def dijkstra(positions, corrupted, start):
    dist = {}
    prev = {}
    Q = []
    removed = set()
    dist[start] = 0
    prev[start] = None
    for pos in positions:
        if (pos in corrupted): continue
        if (pos != start): dist[pos] = sys.maxsize
        hq.heappush(Q, (dist[pos], pos))
    
    while (len(Q) > 0):
        popped = hq.heappop(Q)
        if (popped in removed): continue
        u = popped[1]

        for v in get_adjacent(u):
            if (v not in positions or v in corrupted): continue
            alt = dist[u] + 1
            if (alt < dist[v]):
                removed.add((dist[v], v))
                dist[v] = alt
                prev[v] = u
                hq.heappush(Q, (dist[v], v))
    
    return dist, prev

def get_adjacent(pos): return [
    (pos[0] + 1, pos[1]),
    (pos[0], pos[1] + 1),
    (pos[0] - 1, pos[1]),
    (pos[0], pos[1] - 1)
]

def get_initial_parameters(input, end):
    lines = input.split("\n")
    corrupted = []
    for line in lines:
        nums = re.findall(r"\d+", line)
        corrupted.append((int(nums[0]), int(nums[1])))

    positions = set()
    for x in range(end + 1):
        for y in range(end + 1):
            positions.add((x, y))
    return corrupted, positions

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

def test_part02_sample():
    assert '6,1' == part02(sample, 12, 6)

def test_part02_input():
    with open("src/inputs/day18.txt", "r") as f:
        assert '58,44' == part02(f.read(), 1024, 70)