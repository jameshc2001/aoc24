
def part01(input):
    disk = []
    for index, blocks in enumerate(input):
        if (index % 2 == 0): #used space
            id = index // 2
            for _ in range(int(blocks)): disk.append(str(id))
        else: #free space
            for _ in range(int(blocks)): disk.append('.')
    
    first_free_space = 0
    while(True):
        try: first_free_space = disk.index('.', first_free_space)
        except ValueError: break            
        last = disk.pop()
        if (last != '.'): disk[first_free_space] = last

    return sum([index * int(id) for index, id in enumerate(disk)])

#TESTS

sample = "2333133121414131402"

def test_part01_sample():
    assert 1928 == part01(sample)

def test_part01_input():
    with open("src/inputs/day09.txt", "r") as f:
        assert 6359213660505 == part01(f.read())