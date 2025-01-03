init_type = (-1, -1)


def is_in_bounds(data, pos):
    return 0 <= pos[0] < len(data[0]) and 0 <= pos[1] < len(data)


def explore(x, y, data):
    queue = {(x, y)}
    plant = data[y][x]
    area = {(x, y)}
    perimeter_list = []
    while len(queue) != 0:
        x, y = queue.pop()
        if data[y][x] == plant:
            area.add((x, y))
        for pos in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if not is_in_bounds(data, pos) or (data[pos[1]][pos[0]] != plant and pos not in area):
                perimeter_list.append(pos)
            elif pos not in area:
                queue.add(pos)
    return area, perimeter_list


def check_corner_edge_case(diag, map, tile, tiles):
    check_a = (tile[0], diag[1])
    check_b = (diag[0], tile[1])
    if not is_in_bounds(map, check_a) and not is_in_bounds(map, check_b) or \
            not is_in_bounds(map, check_a) and check_b not in tiles or \
            not is_in_bounds(map, check_b) and check_a not in tiles:
        return True
    try:
        return check_a not in tiles and check_b not in tiles
    except IndexError:
        return False


def check_corner(diag, map, tile, tiles):
    check_a = (tile[0], diag[1])
    check_b = (diag[0], tile[1])
    if not is_in_bounds(map, check_a) and not is_in_bounds(map, check_b) or \
            not is_in_bounds(map, check_a) and check_b not in tiles or \
            not is_in_bounds(map, check_b) and check_a not in tiles:
        return True
    try:
        return (check_a not in tiles and check_b not in tiles) or (check_a in tiles and check_b in tiles)
    except IndexError:
        return False


def count_corners(map, tiles):
    corners = 0
    for tile in tiles:
        x, y = tile
        for diag in [(x + 1, y + 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1)]:
            if diag not in tiles and check_corner(diag, map, tile, tiles) or diag in tiles and check_corner_edge_case(
                    diag, map, tile, tiles):
                corners += 1

    return corners


with open("day12.txt") as f:
    data = [list(line.replace("\n", "")) for line in f.readlines()]
    part1 = 0
    part2 = 0
    explored = {init_type}
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            if (x, y) not in explored:
                tiles, borders = explore(x, y, data)
                area = len(tiles)
                perimeter = len(borders)
                explored.update(tiles)
                part1 += area * perimeter
                part2 += area * count_corners(data, tiles)
    print(part1)
    print(part2)
