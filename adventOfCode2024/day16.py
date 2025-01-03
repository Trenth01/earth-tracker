from collections import deque

dx_dy = [(1, 0), (0, 1), (0, -1), (-1, 0)]
barrier = '#'
start_char = 'S'
end_char = 'E'
empty_space = '.'


def find_pos(maze, char):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == char:
                return x, y
    return None


def mark_best_path_tiles(maze, best_paths):
    marked_maze = [row[:] for row in maze]
    best_seats = {(find_pos(maze, start_char)), (find_pos(maze,end_char))}
    for path in best_paths:
        for x, y in path:
            if marked_maze[y][x] not in (start_char, end_char):
                best_seats.add((x, y))
                marked_maze[y][x] = 'O'

    for row in marked_maze:
        print("".join(row))
    return len(best_seats)


def calculate_min_path(maze):
    start_x, start_y = find_pos(maze, start_char)
    start_dir = 0
    costs = [[-1 for _ in range(len(maze[0]))] for _ in range(len(maze))]
    queue = deque()
    best_paths = []
    min_cost = -1
    for i, (dx, dy) in enumerate(dx_dy):
        if maze[start_y + dy][start_x + dx] != barrier:
            queue.append((start_x + dx, start_y + dy, i, 1 if i == start_dir else 1001, 0, [(start_x, start_y)]))
    while queue:
        x, y, dir, d_cost, cost, path = queue.popleft()
        dx, dy = dx_dy[dir]
        if costs[y][x] == -1 or cost < costs[y][x]:
            costs[y][x] = cost
        elif cost > costs[y][x] + 1002:
            continue
        if (x + dx, y + dy) in path or (x, y) in path:
            continue
        else:
            for i, (dx, dy) in enumerate(dx_dy):
                if maze[y + dy][x + dx] == end_char:
                    path_cost = cost + d_cost + 1
                    if path_cost < min_cost or min_cost == -1:
                        min_cost = path_cost
                        best_paths = [path + [(x, y), (x + dx, y + dy)]]
                    elif path_cost == min_cost:
                        best_paths.append(path + [(x, y), (x + dx, y + dy)])
                elif maze[y + dy][x + dx] != barrier:
                    queue.append((x + dx, y + dy, i, 1 if i == dir else 1001, cost + d_cost, path + [(x, y)]))
    return min_cost, best_paths


def main():
    with open("day16.txt") as input_file:
        maze = [list(x) for x in input_file.read().split('\n')]
        min_cost, best_paths = calculate_min_path(maze)
        print("Part 1:", min_cost)
        print("\nPart 2:")
        marked_maze = mark_best_path_tiles(maze, best_paths)
        print(marked_maze)

main()