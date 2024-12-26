def solution(input, iterations):
    rocks = [int(rock) for rock in input.split(" ")]

    for _ in range(iterations):
        new_rocks = []
        for rock in rocks:
            if (rock == 0): new_rocks.append(1)
            elif (len(str(rock)) % 2 != 0): new_rocks.append(rock * 2024)
            else:
                rock_text = str(rock)
                new_rocks.append(int(rock_text[:len(rock_text) // 2]))
                new_rocks.append(int(rock_text[len(rock_text) // 2:]))
        rocks = new_rocks

    return len(rocks)

#TESTS

sample = "125 17"

def test_part01_sample():
    assert 55312 == solution(sample, 25)

def test_part01_input():
    with open("src/inputs/day11.txt", "r") as f:
        assert 211306 == solution(f.read(), 25)

def test_part02_input():
    with open("src/inputs/day11.txt", "r") as f:
        assert 211306 == solution(f.read(), 75)