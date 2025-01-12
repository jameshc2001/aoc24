from collections import defaultdict
from itertools import combinations
from functools import cache

def part01(input):
    graph = get_graph(input)
    three_cliques = set()
    for node, neighbours in graph.items():
        if (node[0] != 't'): continue

        combos = list(combinations(neighbours, 2))
        for a, b in combos:
            if (a in graph[b]):
                three_cliques.add(frozenset([node, a, b]))

    return len(three_cliques)


def part02(input):
    graph = get_graph(input)

    @cache
    def largest_clique_for_node(node, current_clique=frozenset()):
        if (len(current_clique) > 0):
            for other in current_clique:
                if (node not in graph[other]): return current_clique

        new_clique = frozenset(list(current_clique) + [node])
        largest = new_clique
        for other in graph[node]:
            if (other in new_clique): continue
            
            maybe_largest = largest_clique_for_node(other, new_clique)
            if (len(maybe_largest) > len(largest)):
                largest = maybe_largest
        
        return largest

    largest = frozenset()
    for node in graph.keys():
        maybe_largest = largest_clique_for_node(node)
        if (len(maybe_largest) > len(largest)):
            largest = maybe_largest
    
    return ','.join(sorted(largest))

def get_graph(input):
    graph = defaultdict(set)
    for line in input.split("\n"):
        left, right = line.split("-")
        graph[left].add(right)
        graph[right].add(left)
    graph = dict(graph)
    return graph

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

def test_part02_sample():
    assert "co,de,ka,ta" == part02(sample)

def test_part02_input():
    with open("src/inputs/day23.txt", "r") as f:
        assert "ac,ed,fh,kd,lf,mb,om,pe,qt,uo,uy,vr,wg" == part02(f.read())