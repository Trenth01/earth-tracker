from heapq import heappop, heappush

dx_dy = [(1, 0), (0, 1), (0, -1), (-1, 0)]
barrier = '#'
start_char = 'S'
end_char = 'E'
empty_space = '.'


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


def count_cheats(costs, maze):
    cheats = 0

    for pos, cost in costs.items():
        for dx in range(-20, 21):
            for dy in range(-20, 21):
                if abs(dx) + abs(dy) > 20:  # Skip positions beyond 20 steps
                    continue
                check_pos = (pos[0] + dx, pos[1] + dy)
                if not is_in_bounds(maze, check_pos) or check_pos not in costs:
                    continue
                cheat_value = costs[check_pos] - costs[pos]
                if cheat_value > 100:
                    cheats += 1
    return cheats


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
            return count_cheats(costs, maze)

        for dx, dy in dx_dy:
            nx, ny = x + dx, y + dy
            if is_in_bounds(maze, (nx, ny)) and maze[ny][nx] != barrier:
                new_cost = current_cost + 1
                if (nx, ny) not in costs or new_cost < costs[(nx, ny)]:
                    costs[(nx, ny)] = new_cost
                    priority = new_cost + heuristic((nx, ny), end)
                    heappush(pq, (priority, new_cost, (nx, ny)))

    return -1


def main():
    with open("day20.txt") as input_file:
        maze = [list(x) for x in input_file.read().split('\n')]
        for l in maze:
            print(l)

        min_cost = calculate_min_path(maze)
        print(min_cost)
        # print("Part 1:", min_cost)


main()
