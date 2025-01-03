import re

from statistics import variance

map_height = 103
map_width = 101
quad_counts = [0, 0, 0, 0]


def find_quad(position):
    x, y = position
    mid_x = (map_width - 1) / 2
    mid_y = (map_height - 1) / 2
    if x == mid_x or y == mid_y:
        return None
    if x < mid_x and y < mid_y:
        return 0
    if x < mid_x and y > mid_y:
        return 3
    if x > mid_x and y < mid_y:
        return 1
    if x > mid_x and y > mid_y:
        return 2


def update_robots(robots, i):
    updated_robots = []
    for robot in robots:
        position, velocity = robot
        updated_robots.append(
            [(position[0] + i * velocity[0]) % map_width, (position[1] + i * velocity[1]) % map_height])
    return updated_robots


# Load the data
with open("day14.txt") as file:
    robots = [[[int(a) for a in z.split(',')] for z in y.split(" ")] for y in
              [re.sub('[^0-9,\s-]', '', x.replace('\n', '')) for x in file.readlines()]]

part_1 = update_robots(robots, 100)
for pos in part_1:
    quad = find_quad(pos)
    if quad is not None:
        quad_counts[quad] += 1

print("Part 1:", quad_counts[0] * quad_counts[1] * quad_counts[2] * quad_counts[3])

best_x, best_xvar, best_y, best_yvar = 0, 10 * 100, 0, 10 * 100
for t in range(max(map_width, map_height)):
    xs, ys = zip(*update_robots(robots, t))
    if (xvar := variance(xs)) < best_xvar:
        best_x, best_xvar = t, xvar
    if (yvar := variance(ys)) < best_yvar:
        best_y, best_yvar = t, yvar
print("Part 2:", best_x + ((pow(map_width, -1, map_height) * (best_y - best_x)) % map_height) * map_width)
