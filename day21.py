from copy import deepcopy


def get_monkey_yell(name):
    global monkeys
    if isinstance(monkeys[name], int):
        return monkeys[name]
    equation = monkeys[name]
    op = equation[1]
    left = get_monkey_yell(equation[0])
    right = get_monkey_yell(equation[2])
    if op != "=":
        result = eval("%s %s %s" % (str(left), op, str(right)))
        monkeys[name] = result
    elif left == right:
        return 0
    else:
        return -1
    return result


def get_full_equation(name):
    global monkeys
    if isinstance(monkeys[name], int):
        return str(monkeys[name])
    if isinstance(monkeys[name], str):
        return monkeys[name]
    equation = monkeys[name]
    left = get_full_equation(equation[0])
    op = equation[1]
    right = get_full_equation(equation[2])
    result = "(%s %s %s)" % (left, op, right)
    if "X" not in result:
        monkeys[name] = eval(result)
        result = str(monkeys[name])
    return result


def solve_for_x(x_side, y_side):
    while x_side != "X":
        x_side = x_side[1:-1]
        ends = x_side.split()
        if ends[0] == "X":
            op = ends[1]
            amount = int(ends[2])
            x_side = "X"
        elif ends[-1] == "X":
            op = ends[1]
            amount = int(ends[0])
            x_side = "X"
        elif "(" not in ends[0]:
            amount = int(ends[0])
            op = ends[1]
            x_side = " ".join(ends[2:])
        elif ")" not in ends[-1]:
            amount = int(ends[-1])
            op = ends[-2]
            x_side = " ".join(ends[:-2])
        else:
            print("ERROR!")
            print(ends)
            return -1
        if op == "+":
            print("\tSubtracting %d from both sides" % amount)
            y_side -= amount
        elif op == "-":
            print("\tAdding %d to both sides" % amount)
            y_side += amount
        elif op == "*":
            print("\tDividing both sides by %d" % amount)
            y_side //= amount
        elif op == "//":
            print("\tMultiplying both sides by %d" % amount)
            y_side *= amount
        else:
            print("ERROR!")
            print(ends)
            return -1
        print("%s = %d" % (x_side, y_side))
    return y_side


init = {}
for line in open("day21.txt"):
    (monkey, yell) = line.strip().split(":")
    if yell.strip().isnumeric():
        init[monkey] = int(yell.strip())
    else:
        init[monkey] = yell.strip().split()
        if init[monkey][1] == "/":
            init[monkey][1] = "//"
monkeys = deepcopy(init)
print("Part One: %d" % get_monkey_yell("root"))

monkeys = deepcopy(init)
monkeys["root"][1] = "="
monkeys["humn"] = "X"
left = get_full_equation(monkeys["root"][0])
right = get_full_equation(monkeys["root"][2])
if "X" not in left:
    print("%d = %s" % (eval(left), right))
    part_2 = solve_for_x(x_side=right, y_side=eval(left))
if "X" not in right:
    print("%s = %d" % (left, eval(right)))
    part_2 = solve_for_x(x_side=left, y_side=eval(right))
# 9535830990200 is too high
# 3247317268284 is solution -- how to calculate?
print("Part Two: %d" % part_2)
monkeys["humn"] = part_2
print(get_monkey_yell("root"))

monkeys = deepcopy(init)
monkeys["root"][1] = "="
monkeys["humn"] = 3247317268284
left = get_full_equation(monkeys["root"][0])
right = get_full_equation(monkeys["root"][2])
print((eval(left) - eval(right)))
print(get_monkey_yell("root"))
