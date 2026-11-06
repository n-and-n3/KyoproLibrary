def next_partation(array: list[int]) -> bool:
    s = 0
    for i in range(len(array) - 1, -1, -1):
        if array[i] == 1:
            array.pop()
            s += 1
        else:
            array[i] -= 1
            s += 1
            while s > 0:
                x = min(s, array[i])
                array.append(x)
                s -= x
            return True
    array.append(s)
    return False
