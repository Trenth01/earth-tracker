directions = {'<': (-1, 0), 'v': (0, 1), '^': (0, -1), '>': (1, 0)}


def find_position(map):
    x = -1
    y = -1
    for x in range(0, len(map[0])):
        for y in range(0, len(map)):
            if map[y][x] == '@':
                return x, y
    return x, y


def generate_part2_map(map):
    new_map = []
    for line in map:
        new_map.append(list("".join(line).replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')))
    return new_map


def push_boxes(map, dx_dy, pos):
    current_char = map[pos[1]][pos[0]]
    i = 1
    while current_char == 'O':
        current_char = map[pos[1] + (i * dx_dy[1])][pos[0] + (i * dx_dy[0])]
        i += 1
    if current_char == '#':
        return map, (pos[0] - dx_dy[0], pos[1] - dx_dy[1])
    else:
        map[pos[1] + ((i - 1) * dx_dy[1])][pos[0] + ((i - 1) * dx_dy[0])] = 'O'
        map[pos[1]][pos[0]] = '.'
        return map, pos


def push_large_boxes(map, dx_dy, pos):
    current_char = map[pos[1]][pos[0]]
    i = 1
    dx, dy = dx_dy
    if dy == 0:
        while current_char in ['[', ']']:
            current_char = map[pos[1] + (i * dx_dy[1])][pos[0] + (i * dx_dy[0])]
            i += 1
        if current_char == '#':
            return map, (pos[0] - dx_dy[0], pos[1] - dx_dy[1])
        else:
            map[pos[1] + ((i - 1) * dx_dy[1])].pop(pos[0] + ((i - 1) * dx_dy[0]))
            map[pos[1]].insert(pos[0], '.')
            return map, pos
    else:
        queue = {pos}
        checked = {pos}
        while len(queue) != 0:
            x, y = queue.pop()
            checked.add((x, y))
            current_char = map[y][x]
            if current_char == '[' and (x + 1, y) not in checked:
                queue.add((x + 1, y))
            elif current_char == ']' and (x - 1, y) not in checked:
                queue.add((x - 1, y))
            vertical_char = map[y + dy][x]
            if vertical_char == '#':
                return map, (pos[0] - dx, pos[1] - dy)
            elif vertical_char in ['[', ']'] and (x, y + dy) not in checked:
                queue.add((x, y + dy))
        for large_box in sorted(list(checked), key=lambda tup: tup[1], reverse=(dy == 1)):
            bx, by = large_box
            tmp = map[by + dy][bx]
            map[by + dy][bx] = map[by][bx]
            map[by][bx] = tmp
        return map, pos


def main():
    with open("day15.txt") as f:
        map, instructions = f.read().split('\n\n')
        map = [list(x) for x in map.split('\n')]
        instructions = instructions.replace('\n', '')
        current_pos = find_position(map)
        part2_map = generate_part2_map(map)
        for instruction in list(instructions):
            check_pos = (current_pos[0] + directions[instruction][0], current_pos[1] + directions[instruction][1])
            check_char = map[check_pos[1]][check_pos[0]]
            if check_char == '#':
                continue
            elif check_char == '.':
                current_pos = check_pos
                continue
            else:
                map, current_pos = push_boxes(map, directions[instruction], check_pos)
        part_1 = 0
        for x in range(0, len(map[0])):
            for y in range(0, len(map)):
                if map[y][x] == 'O':
                    part_1 += 100 * y + x
        print(part_1)
        current_pos = find_position(part2_map)
        part2_map[current_pos[1]][current_pos[0]] = '.'
        for instruction in list(instructions):
            check_pos = (current_pos[0] + directions[instruction][0], current_pos[1] + directions[instruction][1])
            check_char = part2_map[check_pos[1]][check_pos[0]]
            if check_char == '.':
                current_pos = check_pos
            elif check_char != '#':
                part2_map, current_pos = push_large_boxes(part2_map, directions[instruction], check_pos)
        part_2 = 0
        for x in range(0, len(part2_map[0])):
            for y in range(0, len(part2_map)):
                if part2_map[y][x] == '[' and x <= len(part2_map[0]) / 2:
                    part_2 += 100 * y + x
                elif part2_map[y][x] == '[' and x > len(part2_map[0]) / 2:
                    part_2 += 100 * y + x
        print(part_2)


main()
