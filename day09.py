with open("day09.txt") as reader:
    lines = reader.readlines()

knots = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
visited_part_one = set([(0, 0)])
visited_part_two = set([(0, 0)])

for line in lines:
    (direction, step_count) = line.strip().split()
    if direction == "R":
        tup = (1, 0)
    elif direction == "L":
        tup = (-1, 0)
    elif direction == "D":
        tup = (0, 1)
    elif direction == "U":
        tup = (0, -1)
    for step in range(int(step_count)):
        knots[0] = tuple(map(sum, zip(knots[0], tup)))
        for i in range(1, len(knots)):
            x_diff = knots[i-1][0] - knots[i][0]
            y_diff = knots[i-1][1] - knots[i][1]
            x_move = 0
            y_move = 0
            if abs(x_diff) > 1 and y_diff == 0:
                x_move = x_diff // abs(x_diff)
            elif abs(y_diff) > 1 and x_diff == 0:
                y_move = y_diff // abs(y_diff)
            elif abs(x_diff) + abs(y_diff) > 2:
                x_move = x_diff // abs(x_diff)
                y_move = y_diff // abs(y_diff)
            knots[i] = tuple(map(sum, zip(knots[i], (x_move, y_move))))
        visited_part_one.add(knots[1])
        visited_part_two.add(knots[9])

print("Part One: %d" % len(visited_part_one))
print("Part Two: %d" % len(visited_part_two))
