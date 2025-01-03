def test_pair(key, lock):
    a = [list(x) for x in key]
    b = [list(x) for x in lock]
    for y, row in enumerate(a):
        for x, _ in enumerate(row):
            if a[y][x] + b[y][x] == '##':
                return 0
    return 1


with open("day25.txt") as input_file:
    inputs = [x.split('\n') for x in input_file.read().split('\n\n')]
    keys = []
    locks = []
    for i in inputs:
        if i[0] == '#' * 5:
            locks.append(i)
        else:
            keys.append(i)
    total = 0
    for lock in locks:
        for key in keys:
            total += test_pair(key, lock)
    print(total)
