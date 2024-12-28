
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

class Box():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def move(self, direction):
        left = (self.left[0] + direction[0], self.left[1] + direction[1])
        right = (self.right[0] + direction[0], self.right[1] + direction[1])
        return Box(left, right)

def part02(input):
    map_input, instructions_input = input.split("\n\n")
    map_input = map_input.replace(".", "..")
    map_input = map_input.replace("O", "[]")
    map_input = map_input.replace("@", "@.")
    map_input = map_input.replace("#", "##")
    instructions = instructions_input.replace("\n", "")
    robot = (-1, -1)
    walls = set()
    boxes = {}
    for y, line in enumerate(map_input.split("\n")):
        for x, character in enumerate(line):
            if (character == '['):
                left = (x, y)
                right = (x + 1, y)
                box = Box(left, right)
                boxes[left] = box
                boxes[right] = box
            elif (character == '#'): walls.add((x, y))
            elif (character == '@'): robot = (x, y)

    for instruction in instructions:
        direction = get_direction(instruction)
        next_pos = (robot[0] + direction[0], robot[1] + direction[1])
        if (next_pos in walls): continue
        elif (next_pos not in boxes): robot = next_pos
        else:
            box_group = set()
            if (not recursive_box_search(next_pos, direction, box_group, boxes, walls)): continue #wall found
            for box in box_group:
                boxes.pop(box.left)
                boxes.pop(box.right)
            for box in box_group:
                moved_box = box.move(direction)
                boxes[moved_box.left] = moved_box
                boxes[moved_box.right] = moved_box
            robot = next_pos

    return sum([100 * box.left[1] + box.left[0] for box in boxes.values()]) // 2

def recursive_box_search(pos, direction, box_group, boxes, walls):
    if (pos in walls): return False
    
    if (pos in boxes):
        new_box = boxes[pos]
        if (new_box in box_group): return True
        box_group.add(new_box)
        moved_box = new_box.move(direction)
        if (not recursive_box_search(moved_box.left, direction,box_group, boxes, walls)): return False #wall found
        if (not recursive_box_search(moved_box.right, direction, box_group, boxes, walls)): return False #wall found

    return True #no wall found

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

def test_part02_advanced_sample():
    assert 9021 == part02(advanced_sample)

def test_part02_input():
    with open("src/inputs/day15.txt", "r") as f:
        assert 1429299 == part02(f.read())