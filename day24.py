def solve(start_time, start_row_index, start_col_index, end_row_index, end_col_index):
    global width, height
    branches = [(start_row_index, start_col_index, start_time)]
    visited = set()
    while len(branches) > 0:
        row_index, col_index, minutes = branches.pop(0)
        if row_index == end_row_index and col_index == end_col_index:
            return minutes
        for next_row_index, next_col_index in [(row_index, col_index), (row_index-1, col_index),
                                               (row_index+1, col_index), (row_index, col_index-1),
                                               (row_index, col_index+1)]:
            if not -1 <= next_row_index <= height or not -1 <= next_col_index <= width or \
                    valley[next_row_index + 1][next_col_index + 1] == '#':
                # Out of bounds
                continue
            if 0 <= next_col_index < width and (
                    (next_row_index - minutes - 1) % height in s_blizzards[next_col_index] or
                    (next_row_index + minutes + 1) % height in n_blizzards[next_col_index]):
                # Collide with a north-bound or south-bound blizzard
                continue
            if 0 <= next_row_index < height and (
                    (next_col_index - minutes - 1) % width in e_blizzards[next_row_index] or
                    (next_col_index + minutes + 1) % width in w_blizzards[next_row_index]):
                # Collide with an east-bound or west-bound blizzard
                continue
            if (next_row_index, next_col_index, (minutes + 1) % (width * height)) in visited:
                # We've seen this before
                continue
            visited.add((next_row_index, next_col_index, (minutes + 1) % (width * height)))
            branches.append((next_row_index, next_col_index, minutes + 1))


valley = open("day24.txt").read().splitlines()
height, width = len(valley) - 2, len(valley[0]) - 2
n_blizzards, s_blizzards = ([set(y for y in range(height) if valley[y + 1][x + 1] == c) for x in range(width)]
                            for c in '^v')
w_blizzards, e_blizzards = ([set(x for x in range(width) if valley[y + 1][x + 1] == c) for y in range(height)]
                            for c in '<>')
minutes_there = solve(0, -1, 0, height, width - 1)
print("Part One: %d" % minutes_there)
minutes_back = solve(minutes_there, height, width - 1, -1, 0)
minutes_there_again = solve(minutes_back, -1, 0, height, width - 1)
print("Part Two: %d" % minutes_there_again)
