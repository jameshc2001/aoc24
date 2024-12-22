import re
from functools import cmp_to_key

def part01(input):
    updates, compare = get_updates_and_compare_function(input)
    correct_updates = [update for update in updates if (sorted(update, key=cmp_to_key(compare)) == update)]
    return sum([update[len(update) // 2] for update in correct_updates])

def part02(input):
    updates, compare = get_updates_and_compare_function(input)
    sorted_updates = [sorted(update, key=cmp_to_key(compare)) for update in updates]
    corrected_updates = [update for index, update in enumerate(sorted_updates) if update != updates[index]]
    return sum([update[len(update) // 2] for update in corrected_updates])

def get_updates_and_compare_function(input):
    rules, updates_text = [text.split("\n") for text in input.split("\n\n")]
    updates = [[int(num) for num in re.findall(r"\d+", update)] for update in updates_text]
    compare = get_compare_func(rules)
    return updates, compare

def get_compare_func(rules):
    after = {}
    before = {}

    for rule in rules:
        left, right = [int(part) for part in rule.split("|")]
        after[left] = after.get(left, []) + [right]
        before[right] = before.get(right, []) + [left]
    
    def compare(a, b):
        next_values = after.get(a, [])
        prev_values = before.get(a, [])
        if (b in next_values): return -1
        if (b in prev_values): return 1
        return 0
    
    return compare

#TESTS

sample = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

def test_part01_sample():
    assert 143 == part01(sample)

def test_part01_input():
    with open("src/inputs/day05.txt", "r") as f:
        assert 4578 == part01(f.read())

def test_part02_sample():
    assert 123 == part02(sample)

def test_part02_input():
    with open("src/inputs/day05.txt", "r") as f:
        assert 6179 == part02(f.read())