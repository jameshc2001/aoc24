import re
import math

def part01(input):
    registers, program = get_registers_and_program(input)
    output = run_program(registers, program)
    return ','.join([str(num) for num in output])

def part02(input):
    _, program = get_registers_and_program(input)
    input = []
    for _ in range(len(program)):
        input.append(0)
    search(input, program, 0)
    return oct_to_decimal(input)

def search(input, program, index):
    if (index == len(program)): return True

    for octal in range(8):
        input[index] = octal
        registers = { 'A': oct_to_decimal(input), 'B': 0, 'C': 0 }
        output = run_program(registers, program)
        if (len(output) == len(program) and output[-index - 1] == program[-index - 1]):
            if (search(input, program, index + 1)): return True
    
    input[index] = 0
    return False

def oct_to_decimal(input):
    input_str = ''.join([str(num) for num in input])
    return int(input_str, 8)

def run_program(registers, program):
    output = []
    pointer = 0
    while (pointer < len(program)):
        opcode = program[pointer]
        operand = program[pointer + 1]
        match opcode:
            case 0: adv(registers, operand)
            case 1: bxl(registers, operand)
            case 2: bst(registers, operand)
            case 3:
                if (jnz(registers)):
                    pointer = operand
                    continue
            case 4: bxc(registers)
            case 5: out(registers, operand, output)
            case 6: bdv(registers, operand)
            case 7: cdv(registers, operand)
        pointer += 2
    return output

def adv(registers, operand):
    registers['A'] = dv(registers, operand)

def bxl(registers, operand):
    registers['B'] = registers['B'] ^ operand

def bst(registers, operand):
    combo = get_combo_operand(registers, operand)
    registers['B'] = combo % 8

def jnz(registers): #if true then jump to literal operand
    return registers['A'] != 0

def bxc(registers):
    registers['B'] = registers['B'] ^ registers['C']

def out(registers, operand, output):
    combo = get_combo_operand(registers, operand)
    output.append(combo % 8)

def bdv(registers, operand):
    registers['B'] = dv(registers, operand)

def cdv(registers, operand):
    registers['C'] = dv(registers, operand)

def dv(registers, operand):
    combo = get_combo_operand(registers, operand)
    return int(registers['A'] / math.pow(2, combo))

def get_combo_operand(registers, operand):
    if (operand <= 3): return operand
    if (operand == 4): return registers['A']
    if (operand == 5): return registers['B']
    if (operand == 6): return registers['C']

def get_registers_and_program(input):
    registers_text, program_text = input.split("\n\n")
    registers_values = [int(num) for num in re.findall(r"\d+", registers_text)]
    registers = { 'A': registers_values[0], 'B': registers_values[1], 'C': registers_values[2] }
    program = [int(num) for num in re.findall(r"\d+", program_text)]
    return registers,program

#TESTS

def test_part01_sample():
    sample = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
    assert "4,6,3,5,6,3,5,2,1,0" == part01(sample)

def test_part01_input():
    with open("src/inputs/day17.txt", "r") as f:
        assert '3,1,5,3,7,4,2,7,5' == part01(f.read())

def test_part02_sample():
    sample = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""
    assert 117440 == part02(sample)

def test_part02_input():
    with open("src/inputs/day17.txt", "r") as f:
        assert 190593310997519 == part02(f.read())