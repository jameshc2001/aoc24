
def part01(input):
    disk = get_disk_part01(input)
    
    first_free_space = 0
    while(True):
        try: first_free_space = disk.index('.', first_free_space)
        except ValueError: break            
        last = disk.pop()
        if (last != '.'): disk[first_free_space] = last

    return sum([index * int(id) for index, id in enumerate(disk)])

def part02(input):
    disk = get_disk_part02(input)
    files = reversed([block for block in disk if block[0] != '.'])

    for file_id, file_size in files:
        for block_index, (block_id, block_size) in enumerate(disk):
            if (block_id != '.' and block_id == file_id): break
            if (block_id == '.' and block_size >= file_size):

                file_index = disk.index((file_id, file_size))

                if (block_index == file_index - 1): #special case for when no files to the left
                    disk[file_index], disk[block_index] = disk[block_index], disk[file_index] #swap with left
                else:
                    disk[file_index] = ('.', file_size) #remove old file
                    disk[block_index] = (file_id, file_size) #move file
                    #maintain spacing
                    remaining_free_space = block_size - file_size
                    disk = disk[0:block_index + 1] + [('.', remaining_free_space)] + disk[block_index + 1:]

                break
    
    #remove duplicate files
    exploded_disk = get_exploded_disk(disk)
    return sum([index * int(id) for index, id in enumerate(exploded_disk) if id != '.'])

def get_exploded_disk(disk):
    exploded_disk = []
    for segment in disk:
        for _ in range(segment[1]): exploded_disk.append(segment[0])
    return exploded_disk

def get_disk_part01(input):
    disk = []
    for index, blocks in enumerate(input):
        if (index % 2 == 0): #used space
            id = index // 2
            for _ in range(int(blocks)): disk.append(str(id))
        else: #free space
            for _ in range(int(blocks)): disk.append('.')
    return disk

def get_disk_part02(input):
    simple_disk = get_disk_part01(input)
    disk = []
    occurrences = 1
    current_block = simple_disk[0]
    for next_block in simple_disk[1:]:
        if (next_block == current_block): occurrences += 1
        else:
            disk.append((current_block, occurrences))
            current_block = next_block
            occurrences = 1
    disk.append((next_block, occurrences))
    return disk

#TESTS

sample = "2333133121414131402"

def test_part01_sample():
    assert 1928 == part01(sample)

def test_part01_input():
    with open("src/inputs/day09.txt", "r") as f:
        assert 6359213660505 == part01(f.read())
  
def test_part02_sample():
    assert 2858 == part02(sample)

def test_part02_special_case():
    assert 169 == part02("1313165")

def test_part02_input():
    with open("src/inputs/day09.txt", "r") as f:
        assert 6381624803796 == part02(f.read())

#took me way too long to realise that because we are moving from right to left
#we do not care about the structure to the right of the current file

#this would be much neater if each block kept track of its position in the 'exploded' disk