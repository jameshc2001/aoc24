from collections import defaultdict
from itertools import combinations

def part01(input):
    graph = defaultdict(set)
    for line in input.split("\n"):
        left, right = line.split("-")
        graph[left].add(right)
        graph[right].add(left)
    graph = dict(graph)
    
    three_cliques = set()
    for node, neighbours in graph.items():
        if (node[0] != 't'): continue

        combos = list(combinations(neighbours, 2))
        for a, b in combos:
            if (a in graph[b]):
                three_cliques.add(frozenset([node, a, b]))

    return len(three_cliques)

#TESTS

sample = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

def test_part01_sample():
    assert 7 == part01(sample)

def test_part01_input():
    with open("src/inputs/day23.txt", "r") as f:
        assert 1512 == part01(f.read())