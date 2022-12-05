import re


def is_complete_overlap(start1, end1, start2, end2):
    if start1 <= start2 and end1 >= end2:
        return True
    if start2 <= start1 and end2 >= end1:
        return True
    return False


def is_partial_overlap(start1, end1, start2, end2):
    if start2 <= end1 <= end2:
        return True
    if start1 <= end2 <= end1:
        return True
    return False


with open("day04.txt") as reader:
    lines = reader.readlines()

overlap_count = 0
partial_count = 0
for line in lines:
    sections = list(map(int, re.split(",|-", line.strip())))
    if is_complete_overlap(sections[0], sections[1], sections[2], sections[3]):
        overlap_count += 1
    if is_partial_overlap(sections[0], sections[1], sections[2], sections[3]):
        partial_count += 1

print("Part One: %d" % overlap_count)
print("Part Two: %d" % partial_count)
