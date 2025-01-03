passcode_pad = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
                 '0': (3, 1), 'A': (3, 2)
}

control_pad = {
                 '^': (0, 1), 'A': (0, 2),
    '<': (1, 0), 'v': (1, 1), '>': (1, 2)
}


def calc_commands(key_pad, command_string):
    current_key = 'A'
    output_string = ''
    for command in list(command_string):
        start_pos = key_pad[current_key]
        dest_pos = key_pad[command]
        dx = start_pos[1] - dest_pos[1]
        dy = start_pos[0] - dest_pos[0]
        while dy:
            output_string += '^' if dy > 0 else 'v'
            dy += -1 if dy > 0 else 1
        while dx:
            output_string += '<' if dx > 0 else '>'
            dx += -1 if dx > 0 else 1

        output_string += 'A'

        current_key = command

    return control_pad, output_string


# 123844
def main():
    with open('day21.txt') as input_file:
        commands = input_file.read().split('\n')
        part1_sum = 0
        for command in commands:
            print(command)
            required_commands = calc_commands(*calc_commands(*calc_commands(passcode_pad, command)))[1]
            print(required_commands, len(required_commands))
            numeric_code = int(command.replace('A', ''))
            part1_sum += numeric_code * len(required_commands)

        print(part1_sum)


main()
