with open("day08.txt") as reader:
    lines = reader.readlines()

rows = []
for line in lines:
    rows.append(list(line.strip()))
cols = [[row[y] for row in rows] for y in range(len(rows[0]))]

count = len(rows) * 2
count += len(cols) * 2
count -= 4
for y in range(1, len(rows) - 1):
    for x in range(1, len(cols) - 1):
        if rows[y][x] > max(rows[y][:x]) or \
                rows[y][x] > max(rows[y][x+1:]) or \
                rows[y][x] > max(cols[x][:y]) or \
                rows[y][x] > max(cols[x][y+1:]):
            count += 1

print("Part One: %d" % count)

checked = []
x = len(cols) // 2
y = len(rows) // 2
direction = (0, -1)
max_score = 0
max_possible = len(rows[y][:x]) * len(rows[y][x+1:]) * len(cols[x][:y]) * len(cols[x][y+1:])
while max_possible > max_score:
    print("Checking (%d, %d)" % (x, y))
    current_height = cols[x][y]
    up = 1
    while y - up > 0 and cols[x][y-up] < current_height:
        up += 1
    down = 1
    while y + down < len(rows) - 1 and cols[x][y+down] < current_height:
        down += 1
    left = 1
    while x - left > 0 and rows[y][x-left] < current_height:
        left += 1
    right = 1
    while x + right < len(cols) - 1 and rows[y][x+right] < current_height:
        right += 1
    current_score = up * down * left * right
    if current_score > max_score:
        max_score = current_score
    checked.append((x, y))
    check_next = tuple(map(sum, zip((x, y), direction)))
    new_direction = (-direction[1], direction[0])
    check_alt = tuple(map(sum, zip((x, y), new_direction)))
    if check_alt in checked:
        x = check_next[0]
        y = check_next[1]
    elif check_next not in checked:
        x = check_alt[0]
        y = check_alt[1]
        direction = new_direction
    max_possible = len(rows[y][:x]) * len(rows[y][x+1:]) * len(cols[x][:y]) * len(cols[x][y+1:])

print("Part Two: %d" % max_score)
