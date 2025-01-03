import re
from sympy import symbols, Eq, solve, Rational

with open("day13.txt") as file:
    inputs = [[[int(y) for y in re.sub('[^0-9\s]', '', x).lstrip().split(" ")] for x in i.split('\n')] for i in
              file.read().split('\n\n')]
    s = 0
    for claw_machine in inputs:
        button_a, button_b, target = claw_machine
        A, B = symbols('A B')
        ax, ay = button_a
        bx, by = button_b
        tx, ty = target
        tx += 10000000000000
        ty += 10000000000000
        eq1 = Eq(ax * A + bx * B, tx)
        eq2 = Eq(ay * A + by * B, ty)
        solutions = solve([eq1, eq2], (A, B))
        # integer_solutions = {k: v if v.is_integer else v * v.q for k, v in solutions.items()}
        if type(solutions[A]) is Rational or type(solutions[B]) is Rational:
            pass
        else:
            s += solutions[A]*3 + solutions[B]
    print(s)