with open("day24.txt") as input_file:
    memory, commands = input_file.read().split('\n\n')
    memory = {x.split(": ")[0]: int(x.split(": ")[1]) for x in memory.split('\n')}
    start_memory = memory.copy().keys()
    commands = [x.split(" -> ") for x in commands.split('\n')]
    while commands:
        instructions, target = commands.pop(0)
        a, gate, b = instructions.split(' ')
        if a not in memory or b not in memory:
            commands.append((instructions, target))
            continue
        elif gate == 'AND':
            memory[target] = 1 if memory[a] and memory[b] else 0
        elif gate == 'OR':
            memory[target] = 1 if memory[b] or memory[a] else 0
        elif gate == 'XOR':
            memory[target] = 1 if memory[b] != memory[a] else 0
    for mem in start_memory:
        del memory[mem]
    binary_int = 0
    i = 0
    # print(memory)
    for x in sorted(memory):
        if x.startswith('z'):
            binary_int += 2 ** i * memory[x]

            i += 1
    print(binary_int)
