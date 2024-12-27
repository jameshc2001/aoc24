from collections import defaultdict

def part01(input):
    regions = get_initial_parameters(input)
    return sum([len(region) * get_region_perimeter(region) for region in regions])

def part02(input):
    regions = get_initial_parameters(input)
    return sum([len(region) * get_region_sides(region) for region in regions])

def get_region_sides(region):
    edges = set()
    for pos in region:
        for x, y, d in get_adjecent_with_dir(pos[0], pos[1]):
            if ((x, y) not in region): edges.add((x, y, d))
    
    sides = 0
    while (len(edges) > 0):
        to_explore = [edges.pop()]
        side = []

        while (len(to_explore) > 0): #build side, removing from edges as we go
            edge = to_explore.pop()
            side.append(edge)
            if (edge in edges): edges.remove(edge)

            (x, y, d) = edge
            adjecents = []
            if (d in ['l', 'r']): adjecents = [(x, y + 1, d), (x, y - 1, d)]
            elif (d in ['d', 'u']): adjecents = [(x + 1, y, d), (x - 1, y, d)]

            for adjecent in adjecents:
                if (adjecent in edges): to_explore.append(adjecent)

        sides += 1

    return sides

#get region edges (x, y, direction) e.g.:
#..AA...
#..AAX..
#X is region edge (4, 1, right)
#once you have a list of region edges you can iterate with
#while(len(region_edges) > 0)
#pop one off, look for neighbours with the same direction but one along,
#add them to a stack and repeat exploring (like in region discovery)

def get_region_perimeter(region):
    edges = 0
    for pos in region:
        for adjecent in get_adjecent(pos[0], pos[1]):
            if (adjecent not in region): edges += 1
    return edges

def get_pos_to_plant(input):
    lines = input.split("\n")
    pos_to_plant = defaultdict(lambda:'.')
    for y, line in enumerate(lines):
        for x, region in enumerate(line):
            pos_to_plant[(x, y)] = region
    return pos_to_plant

def get_initial_parameters(input):
    pos_to_plant = get_pos_to_plant(input)
    visited = set()
    regions = []
    for pos, plant in list(pos_to_plant.items()):
        if (pos in visited): continue
        regions.append(get_region_for_pos(pos_to_plant, visited, pos, plant))
    return regions

def get_region_for_pos(pos_to_plant, visited, pos, plant):
    region = set()
    to_explore = [pos]
    while (len(to_explore) > 0):
        current_pos = to_explore.pop()
        visited.add(current_pos)
        region.add(current_pos)

        for adjecent in get_adjecent(current_pos[0], current_pos[1]):
            if (pos_to_plant[adjecent] == plant and adjecent not in visited):
                to_explore.append(adjecent)
    return region

def get_adjecent(x, y): return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
def get_adjecent_with_dir(x, y): return [(x + 1, y, 'r'), (x - 1, y, 'l'), (x, y + 1, 'd'), (x, y - 1, 'u')]

#TESTS

def test_part01_simple():
    sample = """AAAA
BBCD
BBCC
EEEC"""
    assert 140 == part01(sample)

def test_part01_complex():
    sample = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
    assert 772 == part01(sample)

def test_part01_larger():
    sample = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
    assert 1930 == part01(sample)

def test_part01_input():
    with open("src/inputs/day12.txt", "r") as f:
        assert 1467094 == part01(f.read())

def test_part02_simple01():
    sample = """AAAA
BBCD
BBCC
EEEC"""
    assert 80 == part02(sample)

def test_part02_simple02():
    sample = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
    assert 436 == part02(sample)

def test_part02_simple03():
    sample = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""
    assert 236 == part02(sample)

def test_part02_special_case():
    sample = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""
    assert 368 == part02(sample)

def test_part02_larger():
    sample = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
    assert 1206 == part02(sample)

def test_part02_input():
    with open("src/inputs/day12.txt", "r") as f:
        assert 881182 == part02(f.read())