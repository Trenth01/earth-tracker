with open("day19.txt") as f:
    inp = f.read().split('\n')
    patterns = inp[0].replace(',', '').split(' ')
    towels = inp[2:]
    print(patterns, towels)

    def count_ways(towel, memo):
        if towel in memo:
            return memo[towel]
        if not towel:
            return 1

        total = 0
        for pattern in patterns:
            if towel.startswith(pattern):
                total += count_ways(towel[len(pattern):], memo)

        memo[towel] = total
        return total

    total_count = 0
    for towel in towels:
        memo = {}
        total_count += count_ways(towel, memo)

    print(total_count)