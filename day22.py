from collections import defaultdict
import re


def turn_left():
    global facing, direction
    facing = (facing - 1) % 4
    direction = (direction[1], -direction[0])


def turn_right():
    global facing, direction
    facing = (facing + 1) % 4
    direction = (-direction[1], direction[0])


def turn_around():
    global facing, direction
    facing = (facing + 2) % 4
    direction = (-direction[0], -direction[1])


def get_limits_for_position(pos):
    global layout, known_limits
    if pos not in known_limits.keys():
        (pos_x, pos_y) = pos
        exes = [x for (x, y) in layout.keys() if y == pos_y and layout[(x, y)] in [".", "#"]]
        whys = [y for (x, y) in layout.keys() if x == pos_x and layout[(x, y)] in [".", "#"]]
        known_limits[pos] = (min(exes), max(exes), min(whys), max(whys))
    return known_limits[pos]


def change_test_face(desired):
    global layout
    # 4x4 faces
    #   1
    # 234
    #   56
    # Face 1 to 2
    if desired[1] < 0:
        new_x = desired[0] - 8
        new_x = 3 - new_x
        new_pos = (new_x, 4)
        if layout[new_pos] == "#":
            return None
        turn_around()
        return new_pos
    # Face 1 to 3
    if desired[0] == 7 and desired[1] < 4:
        new_pos = (desired[1] + 4, 4)
        if layout[new_pos] == "#":
            return None
        turn_left()
        return new_pos
    # Face 1 to 4 shouldn't go here
    # Face 1 to 5 shouldn't be possible
    # Face 1 to 6
    if desired[0] == 12 and desired[1] < 4:
        new_y = 3 - desired[1]
        new_y += 8
        new_pos = (15, new_y)
        if layout[new_pos] == "#":
            return None
        turn_around()
        return new_pos
    # Face 2 to 1
    if desired[0] < 4 and desired[1] < 4:
        new_x = 3 - desired[0]
        new_x += 8
        new_pos = (new_x, 0)
        if layout[new_pos] == "#":
            return None
        turn_around()
        return new_pos
    # Face 2 to 3 shouldn't go here
    # Face 2 to 4 shouldn't be possible
    # Face 2 to 5
    if desired[0] < 4 and desired[1] == 8:
        new_x = 3 - desired[0]
        new_x += 8
        new_pos = (new_x, 11)
        if layout[new_pos] == "#":
            return None
        turn_around()
        return new_pos
    # Face 2 to 6
    if desired[0] < 0:
        new_x = 7 - desired[1]
        new_x += 12
        new_pos = (new_x, 11)
        if layout[new_pos] == "#":
            return None
        turn_right()
        return new_pos
    # Face 3 to 1
    if desired[1] == 3 and 3 < desired[0] < 8:
        new_pos = (8, desired[0] - 4)
        if layout[new_pos] == "#":
            return None
        turn_right()
        return new_pos
    # Face 3 to 2 shouldn't go here
    # Face 3 to 4 shouldn't go here
    # Face 3 to 5
    if desired[1] == 9 and 3 < desired[0] < 8:
        new_y = 7 - desired[0]
        new_y += 8
        new_pos = (8, new_y)
        if layout[new_pos] == "#":
            return None
        turn_left()
        return new_pos
    # Face 3 to 6 shouldn't be possible
    # Face 4 to 1 shouldn't go here
    # Face 4 to 2 shouldn't be possible
    # Face 4 to 3 shouldn't go here
    # Face 4 to 5 shouldn't go here
    # Face 4 to 6
    if desired[0] == 12 and 3 < desired[1] < 8:
        new_x = 7 - desired[1]
        new_x += 12
        new_pos = (new_x, 8)
        if layout[new_pos] == "#":
            return None
        turn_right()
        return new_pos
    # Face 5 to 1 shouldn't be possible
    # Face 5 to 2
    if 7 < desired[0] < 12 and desired[1] == 12:
        new_x = desired[0] - 8
        new_x = 3 - new_x
        new_pos = (new_x, 7)
        if layout[new_pos] == "#":
            return None
        turn_around()
        return new_pos
    # Face 5 to 3
    if desired[0] == 7 and desired[1] > 7:
        new_x = desired[1] - 8
        new_x = 7 - new_x
        new_pos = (new_x, 7)
        if layout[new_pos] == "#":
            return None
        turn_right()
        return new_pos
    # Face 5 to 4 shouldn't go here
    # Face 5 to 6 shouldn't go here
    # Face 6 to 1
    if desired[0] == 16:
        new_y = desired[1] - 8
        new_y = 3 - new_y
        new_pos = (11, new_y)
        if layout[new_pos] == "#":
            return None
        turn_around()
        return new_pos
    # Face 6 to 2
    if 11 < desired[0] < 16 and desired[1] > 11:
        new_y = desired[0] - 12
        new_y = 7 - new_y
        new_pos = (0, new_y)
        if layout[new_pos] == "#":
            return None
        turn_left()
        return new_pos
    # Face 6 to 3 shouldn't be possible
    # Face 6 to 4
    if desired[1] == 7 and 11 < desired[0] < 16:
        new_y = desired[0] - 12
        new_y = 7 - new_y
        new_pos = (11, new_y)
        if layout[new_pos] == "#":
            return None
        turn_left()
        return new_pos
    # Face 6 to 5 shouldn't go here


def change_face(desired):
    global layout
    # 50x50 faces
    #  12
    #  3
    # 56
    # 4
    # Face 1 to 2 shouldn't go here
    # Face 1 to 3 shouldn't go here
    # Face 1 to 4
    if desired[1] < 0 and 50 <= desired[0] < 100:
        new_pos = (0, desired[0] + 100)
        if layout[new_pos] == "#":
            return None
        turn_right()
        return new_pos
    # Face 1 to 5
    if desired[0] == 49 and 0 <= desired[1] < 50:
        new_pos = (0, 149 - desired[1])
        if layout[new_pos] == "#":
            return None
        turn_around()
        return new_pos
    # Face 1 to 6 shouldn't be possible
    # Face 2 to 1 shouldn't go here
    # Face 2 to 3
    if desired[1] == 50 and 100 <= desired[0] < 150:
        new_pos = (99, desired[0] - 50)
        if layout[new_pos] == "#":
            return None
        turn_right()
        return new_pos
    # Face 2 to 4
    if desired[1] < 0 and 100 <= desired[0] < 150:
        new_pos = (desired[0] - 100, 199)
        if layout[new_pos] == "#":
            return None
        return new_pos
    # Face 2 to 5 shouldn't be possible
    # Face 2 to 6
    if desired[0] == 150 and 0 <= desired[1] < 50:
        new_pos = (99, 149 - desired[1])
        if layout[new_pos] == "#":
            return None
        turn_around()
        return new_pos
    # Face 3 to 1 shouldn't go here
    # Face 3 to 2
    if desired[0] == 100 and 50 <= desired[1] < 100:
        new_pos = (desired[1] + 50, 49)
        if layout[new_pos] == "#":
            return None
        turn_left()
        return new_pos
    # Face 3 to 4 shouldn't be possible
    # Face 3 to 5
    if desired[0] == 49 and 50 <= desired[1] < 100:
        new_pos = (desired[1] - 50, 100)
        if layout[new_pos] == "#":
            return None
        turn_left()
        return new_pos
    # Face 3 to 6 shouldn't go here
    # Face 4 to 1
    if desired[0] < 0 and 150 <= desired[1] < 200:
        new_pos = (desired[1] - 100, 0)
        if layout[new_pos] == "#":
            return None
        turn_left()
        return new_pos
    # Face 4 to 2
    if desired[1] == 200 and 0 <= desired[0] < 50:
        new_pos = (desired[0] + 100, 0)
        if layout[new_pos] == "#":
            return None
        return new_pos
    # Face 4 to 3 shouldn't be possible
    # Face 4 to 5 shouldn't go here
    # Face 4 to 6
    if desired[0] == 50 and 150 <= desired[1] < 200:
        new_pos = (desired[1] - 100, 149)
        if layout[new_pos] == "#":
            return None
        turn_left()
        return new_pos
    # Face 5 to 1
    if desired[0] < 0 and 100 <= desired[1] < 150:
        new_pos = (50, 149 - desired[1])
        if layout[new_pos] == "#":
            return None
        turn_around()
        return new_pos
    # Face 5 to 2 shouldn't be possible
    # Face 5 to 3
    if desired[1] == 99 and 0 <= desired[0] < 50:
        new_pos = (50, desired[0] + 50)
        if layout[new_pos] == "#":
            return None
        turn_right()
        return new_pos
    # Face 5 to 4 shouldn't go here
    # Face 5 to 6 shouldn't go here
    # Face 6 to 1 shouldn't be possible
    # Face 6 to 2
    if desired[0] == 100 and 100 <= desired[1] < 150:
        new_pos = (149, 149 - desired[1])
        if layout[new_pos] == "#":
            return None
        turn_around()
        return new_pos
    # Face 6 to 3 shouldn't go here
    # Face 6 to 4
    if desired[1] == 150 and 50 <= desired[0] < 100:
        new_pos = (49, desired[0] + 100)
        if layout[new_pos] == "#":
            return None
        turn_right()
        return new_pos
    # Face 6 to 5 shouldn't go here


layout = defaultdict(lambda: " ")
start = None
layout_complete = False
for y, line in enumerate(open("day22.txt")):
    if not layout_complete:
        if len(line.strip()) == 0:
            layout_complete = True
        else:
            for x, char in enumerate(line.rstrip()):
                layout[x, y] = char
                if char == "." and start is None:
                    start = (x, y)
    else:
        route_string = line.strip()
route = re.split("(R|L)", route_string)

position = start
known_limits = {}
facing = 0
direction = (1, 0)
for instruction in route:
    if instruction.isnumeric():
        forward = int(instruction)
        limits = get_limits_for_position(position)
        for step in range(forward):
            next_pos = tuple(map(sum, zip(position, direction)))
            if next_pos[0] < limits[0]:
                next_pos = (limits[1], next_pos[1])
            elif next_pos[0] > limits[1]:
                next_pos = (limits[0], next_pos[1])
            if next_pos[1] < limits[2]:
                next_pos = (next_pos[0], limits[3])
            elif next_pos[1] > limits[3]:
                next_pos = (next_pos[0], limits[2])
            if layout[next_pos] == "#":
                break
            position = next_pos
    else:
        if instruction == "L":
            turn_left()
        elif instruction == "R":
            turn_right()
        else:
            print("ERROR! Unknown instruction: %s" % instruction)
final_row = position[1] + 1
final_col = position[0] + 1
password = (final_row * 1000) + (final_col * 4) + facing
print("Part One: %d" % password)

position = start
facing = 0
direction = (1, 0)
for instruction in route:
    if instruction.isnumeric():
        forward = int(instruction)
        for step in range(forward):
            next_pos = tuple(map(sum, zip(position, direction)))
            if layout[next_pos].isspace():
                # next_pos = change_test_face(next_pos)
                next_pos = change_face(next_pos)
            if next_pos is None or layout[next_pos] == "#":
                break
            position = next_pos
    else:
        if instruction == "L":
            turn_left()
        elif instruction == "R":
            turn_right()
        else:
            print("ERROR! Unknown instruction: %s" % instruction)
final_row = position[1] + 1
final_col = position[0] + 1
password = (final_row * 1000) + (final_col * 4) + facing
print("Part Two: %d" % password)
