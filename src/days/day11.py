from collections import defaultdict

def solution(input, iterations):
    rock_list = [int(rock) for rock in input.split(" ")]
    rocks = defaultdict(lambda:0)
    for rock in rock_list: rocks[rock] += 1

    for _ in range(iterations):
        new_rocks = defaultdict(lambda:0)
        for rock, occurrences in rocks.items():
            if (rock == 0): new_rocks[1] += occurrences
            elif (len(str(rock)) % 2 != 0): new_rocks[rock * 2024] += occurrences
            else:
                rock_text = str(rock)
                new_rocks[int(rock_text[:len(rock_text) // 2])] += occurrences
                new_rocks[int(rock_text[len(rock_text) // 2:])] += occurrences
        rocks = new_rocks

    return sum([occurrences for _, occurrences in rocks.items()])

#TESTS

sample = "125 17"

def test_part01_sample():
    assert 55312 == solution(sample, 25)

def test_part01_input():
    with open("src/inputs/day11.txt", "r") as f:
        assert 211306 == solution(f.read(), 25)

def test_part02_input():
    with open("src/inputs/day11.txt", "r") as f:
        assert 250783680217283 == solution(f.read(), 75)


#we do not care about the ordering of rocks. Have a dictionary of rock -> occurrences.
#iterate through creating a new dictionary of the same type.
#e.g. rock 1 occurs 4 times. Each one creates a new 2024 rock so in the new dictioanry
#increase occurrences of rock 2024 by 4