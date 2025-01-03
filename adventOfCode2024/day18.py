from heapq import heappop, heappush

dx_dy = [(1, 0), (0, 1), (0, -1), (-1, 0)]
barrier = '#'
start_char = 'S'
end_char = 'E'
empty_space = '.'
maze_width = 71
maze_height = 71


def is_in_bounds(data, pos):
    return 0 <= pos[0] < len(data[0]) and 0 <= pos[1] < len(data)


def find_pos(maze, char):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == char:
                return x, y
    return None


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def calculate_min_path(maze):
    start = find_pos(maze, start_char)
    end = find_pos(maze, end_char)

    if not start or not end:
        return -1

    pq = []
    heappush(pq, (0, 0, start))

    visited = set()
    costs = {start: 0}

    while pq:
        total_cost, current_cost, (x, y) = heappop(pq)

        if (x, y) in visited:
            continue
        visited.add((x, y))

        if (x, y) == end:
            return current_cost

        for dx, dy in dx_dy:
            nx, ny = x + dx, y + dy
            if is_in_bounds(maze, (nx, ny)) and maze[ny][nx] != barrier:
                new_cost = current_cost + 1
                if (nx, ny) not in costs or new_cost < costs[(nx, ny)]:
                    costs[(nx, ny)] = new_cost
                    priority = new_cost + heuristic((nx, ny), end)
                    heappush(pq, (priority, new_cost, (nx, ny)))

    return -1


def init_maze(bits):
    maze = [[empty_space for _ in range(maze_width)] for _ in range(maze_height)]
    for bit in bits:
        maze[bit[1]][bit[0]] = barrier
    maze[0][0] = start_char
    maze[maze_height-1][maze_width-1] = end_char
    return maze


def main():
    with open("day18.txt") as input_file:
        min_cost = -1
        bit_positions = [[int(y) for y in x.split(',')] for x in input_file.read().split('\n')]
        num_bits = len(bit_positions)
        print("Part 1:", calculate_min_path(init_maze(bit_positions[:1024])))
        while min_cost == -1:
            maze = init_maze(bit_positions[:num_bits])
            min_cost = calculate_min_path(maze)
            num_bits -= 1
        print("Part 2:", bit_positions[num_bits+1])

main()