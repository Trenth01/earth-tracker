import math


def mix(num1, num2):
    return num1 ^ num2


def prune(num):
    return num % 16777216


with open("day22.txt") as input_file:
    initial_numbers = [int(x) for x in input_file.read().split('\n')]
    secret_sum = 0
    sequences = {str([]): 0}
    for number in initial_numbers:
        secret_num = number
        current_sequence = []
        dx = 0
        for _ in range(2000):
            before = secret_num
            current_sequence.append(dx)
            if len(current_sequence) == 4:
                if str(current_sequence) in sequences:
                    sequences[str(current_sequence)] += secret_num % 10
                else:
                    sequences[str(current_sequence)] = secret_num % 10
                current_sequence = current_sequence[:-1]
            secret_num = prune(mix(secret_num, secret_num * 64))
            secret_num = prune(mix(secret_num, int(math.floor(secret_num / 32))))
            secret_num = prune(mix(secret_num, secret_num * 2048))
            dx = (secret_num - before) % 10
        secret_sum += secret_num
    print(secret_sum)
    print(sorted(sequences.values()))
