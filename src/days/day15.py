
def part01(input):
    map_input, instructions_input = input.split("\n\n")
    instructions = instructions_input.replace("\n", "")
    robot = (-1, -1)
    walls = set()
    boxes = set()
    for y, line in enumerate(map_input.split("\n")):
        for x, character in enumerate(line):
            if (character == 'O'): boxes.add((x, y))
            elif (character == '#'): walls.add((x, y))
            elif (character == '@'): robot = (x, y)

    for instruction in instructions:
        direction = get_direction(instruction)
        next_pos = (robot[0] + direction[0], robot[1] + direction[1])
        if (next_pos in walls): continue
        elif (next_pos not in boxes): robot = next_pos
        else:
            next_free_pos = next_pos
            while (next_free_pos in boxes):
                next_free_pos = (next_free_pos[0] + direction[0], next_free_pos[1] + direction[1])
            
            if (next_free_pos in walls): continue
            else:
                boxes.remove(next_pos)
                boxes.add(next_free_pos)
                robot = next_pos

    return sum([100 * y + x for x, y in boxes])

def part02(input):
    return -1

def get_direction(instruction):
    if (instruction == '<'): return (-1, 0)
    if (instruction == '^'): return (0, -1)
    if (instruction == '>'): return (1, 0)
    if (instruction == 'v'): return (0, 1)


#TESTS

simple_sample = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

advanced_sample = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

def test_part01_simple_sample():
    assert 2028 == part01(simple_sample)

def test_part01_advanced_sample():
    assert 10092 == part01(advanced_sample)

def test_part01_input():
    with open("src/inputs/day15.txt", "r") as f:
        assert 1412971 == part01(f.read())

def test_part02_simple_sample():
    assert 2028 == part02(simple_sample)

def test_part02_advanced_sample():
    assert 10092 == part02(advanced_sample)

def test_part02_input():
    with open("src/inputs/day15.txt", "r") as f:
        assert 1412971 == part02(f.read())