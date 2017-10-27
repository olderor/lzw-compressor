import struct

END_OF_BLOCK = 256
END_OF_DATA = 257
MAX_TABLE_SIZE = 2 ** 16

def get_table():
    table = {}
    for i in range(256):
        table[chr(i)] = i
    return table


def get_table2():
    table = {}
    for i in range(256):
        table[i] = chr(i)
    return table


def compress(bytes):
    text = struct.unpack("B" * len(bytes), bytes)
    if len(text) == 0:
        return []

    result = []
    table = get_table()
    current = ""
    blocks = []
    for char in text:
        total = current + chr(char)

        if total in table:
            current = total
        else:
            result.append(table[current])
            table[total] = len(table)
            current = chr(char)
            if len(table) == MAX_TABLE_SIZE:
                table = get_table()

    result.append(table[current])
    return struct.pack("H" * len(result), *result)


def decompress(packed_data):
    commpressed_data = struct.unpack("H" * (len(packed_data) // 2), packed_data)

    table = get_table2()

    prev = table[commpressed_data[0]]
    commpressed_data = commpressed_data[1:]
    result = prev
    string = ""
    for element in commpressed_data:
        if element in table:
            string = table[element]
        elif element == len(table):
            string = prev + prev[0]
        else:
            return "Failed to decompress"

        result += string
        table[len(table)] = prev + string[0]
        if len(table) == MAX_TABLE_SIZE:
            table = get_table2()
        prev = string

    lst = list(map(ord, result))
    binary = struct.pack("B" * (len(result)), *lst)
    print(len(lst))
    return binary
