from collections import defaultdict


def get_range(start, end):
    low = min(start, end)
    high = max(start, end) + 1
    return list(range(low, high))


def pretty_print():
    global view, left_boundary, right_boundary, floor
    for y in range(floor + 1):
        for x in get_range(left_boundary, right_boundary):
            print(view[(x, y)], end="")
        print()
    print()


with open("day14.txt") as reader:
    lines = reader.readlines()

view = defaultdict(lambda: ".")
for line in lines:
    path_coords = line.strip().split(" -> ")
    prev_coord = None
    for coord in path_coords:
        (x, y) = eval(coord)
        view[(x, y)] = "#"
        if prev_coord is not None:
            for x_delta in get_range(prev_coord[0], x):
                for y_delta in get_range(prev_coord[1], y):
                    view[(x_delta, y_delta)] = "#"
        prev_coord = (x, y)
left_boundary = min([x for (x, y) in view.keys()])
right_boundary = max([x for (x, y) in view.keys()])
floor = max([y for (x, y) in view.keys()])

sand_count = 0
while True:
    sand_coord = (500, 0)
    while True:
        if sand_coord[0] < left_boundary or sand_coord[0] > right_boundary or sand_coord[1] > floor:
            break
        next_coord = tuple(map(sum, zip(sand_coord, (0, 1))))
        if view[next_coord] == ".":
            sand_coord = next_coord
            continue
        next_coord = tuple(map(sum, zip(sand_coord, (-1, 1))))
        if view[next_coord] == ".":
            sand_coord = next_coord
            continue
        next_coord = tuple(map(sum, zip(sand_coord, (1, 1))))
        if view[next_coord] == ".":
            sand_coord = next_coord
            continue
        break
    if sand_coord[0] < left_boundary or sand_coord[0] > right_boundary or sand_coord[1] > floor:
        break
    view[sand_coord] = "O"
    sand_count += 1
print("Part One: %d" % sand_count)

floor += 2
while True:
    sand_coord = (500, 0)
    while True:
        next_coord = tuple(map(sum, zip(sand_coord, (0, 1))))
        if next_coord[1] < floor and view[next_coord] == ".":
            sand_coord = next_coord
            continue
        next_coord = tuple(map(sum, zip(sand_coord, (-1, 1))))
        if next_coord[1] < floor and view[next_coord] == ".":
            sand_coord = next_coord
            continue
        next_coord = tuple(map(sum, zip(sand_coord, (1, 1))))
        if next_coord[1] < floor and view[next_coord] == ".":
            sand_coord = next_coord
            continue
        break
    view[sand_coord] = "O"
    sand_count += 1
    left_boundary = min(left_boundary, sand_coord[0])
    right_boundary = max(right_boundary, sand_coord[0])
    if sand_coord == (500, 0):
        break
print("Part Two: %d" % sand_count)
