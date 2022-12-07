class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.subdirectories = []
        self.files = {}
        self.size = None

    def __repr__(self):
        retval = "Directory: %s\n" % str(self.name)
        retval += "\tParent: %s\n" % str(None if self.parent is None else self.parent.name)
        retval += "\tSubdirectories: %s\n" % str(self.subdirectories)
        retval += "\tFiles: %s\n" % str(self.files)
        return retval

    def new_subdirectory(self, sub_name):
        new_sub = Directory(name=sub_name, parent=self)
        self.subdirectories.append(new_sub)
        return new_sub

    def get_subdirectory(self, sub_name):
        subs = [sub for sub in self.subdirectories if sub.name == sub_name]
        return None if len(subs) == 0 else subs[0]

    def get_subdirectory_names(self):
        return list(sub.name for sub in self.subdirectories)

    def get_size(self):
        if self.size is not None:
            return self.size
        self.size = 0
        for sub in self.subdirectories:
            self.size += sub.get_size()
        self.size += sum(self.files.values())
        return self.size


def get_part_one(directory):
    total = 0
    for sub in directory.subdirectories:
        total += get_part_one(sub)
    size = directory.get_size()
    if size <= 100000:
        total += size
    return total


def get_part_two(directory, best):
    global required
    if best is None or best > directory.get_size() >= required:
        best = directory.get_size()
    if directory.get_size() > required:
        for sub in directory.subdirectories:
            best = get_part_two(sub, best)
    return best


with open("day07.txt") as reader:
    lines = reader.readlines()

sizes = {}
root = Directory(name="/", parent=None)
current_directory = root
for line in lines:
    if line[0] == "$":
        if line[2:4] == "cd":
            new_location = line[5:].strip()
            new_directory = None
            if new_location == "..":
                new_directory = current_directory.parent
            elif new_location == "/":
                new_directory = root
            else:
                new_directory = current_directory.get_subdirectory(new_location)
            current_directory = new_directory
    elif line[0].isnumeric():
        data = line.strip().split()
        current_directory.files.update({data[1]: int(data[0])})
    elif line[:3] == "dir":
        subdir = line.strip()[4:]
        if subdir not in current_directory.get_subdirectory_names():
            current_directory.new_subdirectory(subdir)

part_one = get_part_one(root)
print("Part One: %s" % part_one)

used = root.get_size()
available = 70000000 - used
required = 30000000 - available

part_two = get_part_two(root, None)
print("Part Two: %s" % part_two)
