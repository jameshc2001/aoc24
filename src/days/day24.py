from typing import List

class Gate:
    def __init__(self, left_input, right_input, operation, output):
        self.left_input = left_input
        self.right_input = right_input
        self.operation = operation
        self.output = output

    def output_value(self, left_value, right_value):
        if (self.operation == "AND"): return left_value & right_value
        if (self.operation == "OR"): return left_value | right_value
        if (self.operation == "XOR"): return left_value ^ right_value

def part01(input):

    initial_wires, gate_text = input.split("\n\n")

    wires = {}
    for wire in initial_wires.split("\n"):
        name, value = wire.split(": ")
        wires[name] = int(value)

    gates = list()
    for gate in gate_text.split("\n"):
        left_input, operation, right_input, output = gate.replace("-> ", "").split(" ")
        gates.append(Gate(left_input, right_input, operation, output))


    while (len(gates) > 0):
        remaining_gates = list()
        for gate in gates:
            if (gate.left_input not in wires or gate.right_input not in wires):
                remaining_gates.append(gate)
            else:
                wires[gate.output] = gate.output_value(wires[gate.left_input], wires[gate.right_input])
        gates = remaining_gates

    z_wires = reversed(sorted([(k, v) for k, v in wires.items() if k[0] == "z"], key=lambda x: x[0]))
    binary = ""
    for wire in z_wires: binary += str(wire[1])

    return int(binary, 2)

#TESTS

sample = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

def test_part01_sample():
    assert 2024 == part01(sample)

def test_part01_input():
    with open("src/inputs/day24.txt", "r") as f:
        assert 59336987801432 == part01(f.read())