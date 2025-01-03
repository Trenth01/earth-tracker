import math
import sys

operands = {0: '0', 1: '1', 2: '2', 3: '3', 4: 'A', 5: 'B', 6: 'C', 7: '0'}


def adv(memory, operand):
    memory['A'] = int(memory['A'] // math.pow(2, memory[operands[operand]]))
    return memory, None


def bxl(memory, operand):
    memory['B'] = memory['B'] ^ operand
    return memory, None


def bst(memory, operand):
    memory['B'] = memory[operands[operand]] % 8
    return memory, None


def jnz(memory, operand):
    if memory['A'] == 0:
        return memory, None
    else:
        return memory, operand


def bxc(memory, operand):
    memory['B'] = memory['B'] ^ memory['C']
    return memory, None


def out(memory, operand):
    sys.stdout.write(f'{memory[operands[operand]] % 8},')
    return memory, None


def bdv(memory, operand):
    memory['B'] = int(memory['A'] // math.pow(2, memory[operands[operand]]))
    return memory, None


def cdv(memory, operand):
    memory['C'] = int(memory['A'] // math.pow(2, memory[operands[operand]]))
    return memory, None


opcodes = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}


def main():
    with open("day17.txt") as input_file:
        memory = {v: int(v) if v.isdigit() else v for v in operands.values()}
        instructions = []
        inputs = input_file.read().split('\n')
        for i in inputs:
            if 'Register' in i:
                _, register, val = i.replace(':', '').split(' ')
                memory[register] = int(val)
            elif 'Program' in i:
                instructions = [int(x) for x in i.split(' ')[1].split(',')]
        i = 0
        while i < len(instructions) - 1:
            opcode = instructions[i]
            operand = instructions[i + 1]
            i += 2
            memory, update_i = opcodes[opcode](memory, operand)
            if update_i is not None:
                i = update_i
        sys.stdout.write('\b\n')
        queue = [(0, 0)]
        solutions = []
        # In case anyone ever looks at this again (((A % 8) ^ 3) ^ (A // 2 ** ((A % 8) ^ 3)) ^ 5) % 8 is the pure math
        # representation of the computation preformed by the above code, worked out with pen and paper
        while queue:
            current, depth = queue.pop()
            current_pos = len(instructions) - 1 - depth

            if current_pos < 0:
                solutions.append(current)
                continue

            for j in range(8):
                A = current + j
                if A != 0 and (((A % 8) ^ 3) ^ (A // 2 ** ((A % 8) ^ 3)) ^ 5) % 8 == instructions[current_pos]:
                    if current_pos != 0:
                        queue.append((A * 8, depth + 1))
                    else:
                        solutions.append(A)

        print(sorted(solutions))

main()
