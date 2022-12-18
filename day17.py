def pretty_print(tuples):
    top = max([x for (x, y) in tuples])
    for x in reversed(range(top + 1)):
        if x > 0:
            print("|", end="")
            for y in range(7):
                print("#" if (x, y) in tuples else ".", end="")
            print("|")
        else:
            print("+-------+")
    print()


def get_height_for_iteration(iteration):
    global cycle_length, cycle_height, jet_sequence, jet_cycle, cycles, last_iteration
    remaining = iteration - last_iteration
    full_cycles = remaining // cycle_length
    excess = remaining % cycle_length
    final = height + (full_cycles * cycle_height)
    last_jet = jet_cycle[excess]
    final += (cycles[last_jet][0] - base[0])
    return final


with open("day17.txt") as reader:
    jets = reader.readline().strip()

shapes = [[(0, 2), (0, 3), (0, 4), (0, 5)],
          [(0, 3), (1, 2), (1, 3), (1, 4), (2, 3)],
          [(0, 2), (0, 3), (0, 4), (1, 4), (2, 4)],
          [(0, 2), (1, 2), (2, 2), (3, 2)],
          [(0, 2), (0, 3), (1, 2), (1, 3)]]

chamber = [(0, y) for y in range(7)]
down = (-1, 0)
jet = 0
i = 0
cycles = {}
while True:
    height = max([x for (x, y) in chamber])
    shape_id = i % len(shapes)
    if shape_id == 0 and (jet, shape_id) in cycles.keys():
        base = cycles[(jet, shape_id)]
        cycle_height = height - base[0]
        cycle_length = i - base[1]
        jet_sequence = list(cycles.keys())
        cycle_index = jet_sequence.index((jet, shape_id))
        jet_cycle = jet_sequence[cycle_index:]
        last_iteration = i
        break
    else:
        cycles[(jet, shape_id)] = (height, i)
    shape = shapes[shape_id]
    moved = []
    for t in shape:
        moved.append(tuple(map(sum, zip(t, (height + 4, 0)))))
    stopped = False
    while not stopped:
        direction = (0, -1) if jets[jet] == "<" else (0, 1)
        left_edge = min([y for (x, y) in moved])
        right_edge = max([y for (x, y) in moved])
        if (direction == (0, -1) and left_edge > 0) or (direction == (0, 1) and right_edge < 6):
            moving = []
            for t in moved:
                moving.append(tuple(map(sum, zip(t, direction))))
            if len(set(chamber) - set(moving)) == len(chamber):
                moved = moving
        direction = (-1, 0)
        moved_down = False
        moving = []
        for t in moved:
            moving.append(tuple(map(sum, zip(t, direction))))
        if len(set(chamber) - set(moving)) == len(chamber):
            moved = moving
            moved_down = True
        stopped = not moved_down
        if stopped:
            chamber += moved
        jet = (jet + 1) % len(jets)
    i += 1

if i > 2022:
    print("Part One: %d" % [v for v in cycles.values() if v[1] == 2022][0][0])
else:
    print("Part One: %d" % get_height_for_iteration(2022))

print("Part Two: %d" % get_height_for_iteration(1000000000000))
