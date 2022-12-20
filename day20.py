def solve(decryption_key=1, iterations=1):
    encrypted = {}
    zero_key = -1
    for i, line in enumerate(open("day20.txt")):
        encrypted[i] = int(line.strip()) * decryption_key
        if encrypted[i] == 0:
            zero_key = i
    size = len(encrypted)
    decrypted_indices = list(encrypted.keys())

    for n in range(iterations):
        for k in range(size):
            i = decrypted_indices.index(k)
            v = encrypted[k]
            d = i + v
            d %= (size - 1)
            decrypted_indices.remove(k)
            decrypted_indices.insert(d, k)
    decrypted = [encrypted[k] for k in decrypted_indices]
    zero_index = decrypted_indices.index(zero_key)
    first = (zero_index + 1000) % size
    second = (zero_index + 2000) % size
    third = (zero_index + 3000) % size
    return decrypted[first] + decrypted[second] + decrypted[third]


print("Part One: %d" % solve())
print("Part Two: %d" % solve(decryption_key=811589153, iterations=10))
