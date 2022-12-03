def get_priority(sets):
    shared = sets.pop().intersection(*sets)
    shared_type = shared.pop()

    # ord("Z") = 90, ord("z") = 122
    # ord("A") = 65, ord("a") = 97
    type_val = ord(shared_type)
    if type_val > 90:
        return type_val - 96
    return type_val - 38


with open("day03.txt") as reader:
    lines = reader.readlines()

priority_sum = 0
group_sacks = []
group_sum = 0
for line in lines:
    pack = line.strip()
    mid = int(len(pack) / 2)
    priority_sum += get_priority([set(pack[:mid]), set(pack[mid:])])
    group_sacks.append(set(pack))
    if len(group_sacks) == 3:
        group_sum += get_priority(group_sacks)
        group_sacks = []

print("Part One: %d" % priority_sum)
print("Part Two: %d" % group_sum)
