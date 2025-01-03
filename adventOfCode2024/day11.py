from collections import Counter
import math
import matplotlib.pyplot as plt


def apply_rules(x, count):
    str_x = str(x)
    if x == 0:
        return [{1: count}]
    elif len(str_x) % 2 == 0:
        x_front = str_x[:len(str_x)//2]
        x_back = str_x[len(str_x)//2:]
        return [{math.floor(int(x_front)): count}, {math.floor(int(x_back)): count}]
    else:
        return [{x * 2024: count}]


def blink(frequency_map):
    output = Counter({})
    [[output.update(y) for y in apply_rules(x, frequency_map[x])] for x in frequency_map]
    return output


with open("day11.txt") as file:
    freq_map = Counter([int(x) for x in file.read().replace("\n", "").split(" ")])
    sums = []
    for i in range(0, 100):
        freq_map = blink(freq_map)
        sums.append(sum(
            freq_map[x]
            for x in freq_map
        ))

def plot_scatter(data):
    """
    Generates a scatter plot for a given list of integers.

    Parameters:
        data (list of int): The list of integers to plot.
    """
    if not all(isinstance(i, int) for i in data):
        raise ValueError("All elements in the list must be integers.")
    data_pow = [10 * math.floor(math.log(math.pow(1.6,i))) for i in range(0,100)]


    x = range(len(data))  # Indices for the x-axis
    y = data  # Values for the y-axis


    plt.scatter(x, y, color='blue', label='Data Points')
    plt.scatter(x, data_pow, color='red', label='Pure EXP')
    plt.title('Scatter Plot of List Values')
    plt.xlabel('Blinks')
    plt.ylabel('log(Stones)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

# Example usage:
plot_scatter([10 * math.floor(math.log(x)) for x in sums])