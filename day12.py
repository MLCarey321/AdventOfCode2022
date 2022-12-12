from collections import defaultdict

with open("day12.txt") as reader:
    lines = reader.readlines()

heightmap = {}
row = 0
col = 0
start_point = (0, 0)
destination = (0, 0)
num_rows = len(lines)
num_cols = len(lines[0].strip())
for line in lines:
    col = 0
    for i in list(line.strip()):
        heightmap.update({(col, row): ord(i)})
        if i == "S":
            start_point = (col, row)
            heightmap[(col, row)] = ord("a")
        elif i == "E":
            destination = (col, row)
            heightmap[(col, row)] = ord("z")
        col += 1
    row += 1

shortest = defaultdict(lambda: num_cols * num_rows)
shortest[destination] = 0
while set(heightmap.keys()) != set(shortest.keys()):
    traversed = list(shortest.keys())
    for loc in traversed:
        loc_length = shortest[loc]
        adj = [tuple(map(sum, zip(loc, (0, -1)))), tuple(map(sum, zip(loc, (0, 1)))),
               tuple(map(sum, zip(loc, (-1, 0)))), tuple(map(sum, zip(loc, (1, 0))))]
        for t in [k for k in adj if
                  k not in traversed and min(k) >= 0 and k[0] < num_cols and k[1] < num_rows and heightmap[loc] -
                  heightmap[k] <= 1]:
            shortest[t] = min(loc_length + 1, shortest[t])
    if len(shortest.keys()) == len(traversed):
        break

print("Part One: %d" % shortest[start_point])

a_lengths = [shortest[t] for t in heightmap if heightmap[t] == ord("a")]

print("Part Two: %d" % min(a_lengths))
