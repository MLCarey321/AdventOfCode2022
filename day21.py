from copy import deepcopy


def get_monkey_yell(name):
    global monkeys
    if isinstance(monkeys[name], int) or isinstance(monkeys[name], float):
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
    if isinstance(monkeys[name], int) or isinstance(monkeys[name], float):
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
            amount = float(ends[2])
            x_side = "X"
        elif ends[-1] == "X":
            op = ends[1]
            amount = float(ends[0])
            x_side = "X"
        elif "(" not in ends[0]:
            amount = float(ends[0])
            op = ends[1]
            x_side = " ".join(ends[2:])
        elif ")" not in ends[-1]:
            amount = float(ends[-1])
            op = ends[-2]
            x_side = " ".join(ends[:-2])
        else:
            print("ERROR!")
            print(ends)
            return -1
        if op == "+":
            # print("\tSubtracting %s from both sides" % str(amount))
            y_side -= amount
        elif op == "-":
            if "(" not in ends[0] and ends[0] != "X":
                # print("\t%s - x = y --> x = %s - y" % (str(amount), str(amount)))
                y_side = amount - y_side
            else:
                # print("\tAdding %s to both sides" % str(amount))
                y_side += amount
        elif op == "*":
            # print("\tDividing both sides by %s" % str(amount))
            y_side /= amount
        elif op == "/":
            if "(" not in ends[0] and ends[0] != "X":
                # print("\t%s / x = y --> x = %s / y" % (str(amount), str(amount)))
                y_side = amount / y_side
            else:
                # print("\tMultiplying both sides by %s" % str(amount))
                y_side *= amount
        else:
            print("ERROR!")
            print(ends)
            return -1
        # print("%s = %s" % (x_side, str(y_side)))
    return y_side


init = {}
for line in open("day21.txt"):
    (monkey, yell) = line.strip().split(":")
    if yell.strip().isnumeric():
        init[monkey] = int(yell.strip())
    else:
        init[monkey] = yell.strip().split()
        # if init[monkey][1] == "/":
        #     init[monkey][1] = "//"
monkeys = deepcopy(init)
print("Part One: %d" % get_monkey_yell("root"))

monkeys = deepcopy(init)
monkeys["root"][1] = "="
monkeys["humn"] = "X"
left = get_full_equation(monkeys["root"][0])
right = get_full_equation(monkeys["root"][2])
if "X" not in left:
    # print("%d = %s" % (eval(left), right))
    part_2 = solve_for_x(x_side=right, y_side=eval(left))
if "X" not in right:
    # print("%s = %d" % (left, eval(right)))
    part_2 = solve_for_x(x_side=left, y_side=eval(right))
print("Part Two: %d" % part_2)
