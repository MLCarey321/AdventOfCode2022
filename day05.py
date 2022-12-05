from collections import defaultdict
import re


def process_layer(layer):
    global stacks
    index = 1
    stack_id = 1
    while index < len(layer):
        crate = layer[index]
        if crate.isalpha():
            stacks[stack_id].append(crate)
        index += 4
        stack_id += 1


def process_instruction_9000(instruct):
    # Part One
    global stacks
    ids = list(map(int, filter(None, re.split("\\D", instruct.strip()))))
    for count in range(ids[0]):
        crate = stacks[ids[1]].pop(0)
        stacks[ids[2]].insert(0, crate)


def process_instruction_9001(instruct):
    # Part Two
    global stacks
    ids = list(map(int, filter(None, re.split("\\D", instruct.strip()))))
    moving = stacks[ids[1]][:ids[0]]
    stacks[ids[1]] = stacks[ids[1]][ids[0]:]
    stacks[ids[2]] = moving + stacks[ids[2]]


with open("day05.txt") as reader:
    lines = reader.readlines()

init = True
stacks = defaultdict(list)
for line in lines:
    if len(line.strip()) == 0:
        init = False
    elif init:
        process_layer(line)
    else:
        # process_instruction_9000(line)
        process_instruction_9001(line)

solution = ""
for stack in sorted(stacks.keys()):
    solution += stacks[stack][0]

print("Solution: %s" % solution)
