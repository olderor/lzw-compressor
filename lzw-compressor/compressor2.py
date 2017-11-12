import struct

# TODO: Implement saving filenames.
# TODO: Implement compressing few files into one archive.

#CLEAR_CODE = 256
#END_OF_DATA = 257
TABLE_SIZE = 256
MAX_TABLE_SIZE = 2 ** 32


def get_table():
    table = {}
    for i in range(256):
        table[chr(i)] = i
    #table[CLEAR_CODE] = CLEAR_CODE
    #table[END_OF_DATA] = END_OF_DATA
    return table


def get_table2():
    table = {}
    for i in range(256):
        table[i] = chr(i)
    #table[CLEAR_CODE] = CLEAR_CODE
    #table[END_OF_DATA] = END_OF_DATA
    return table


def copy_to_compress(bytes):
    # TODO: Set flag if compressing was not success.
    #return bytearray([0]) + bytes
    return bytes


def compress(bytes):
    # TODO: Set flag if compressing was success.
    text = struct.unpack("B" * len(bytes), bytes)
    if len(text) == 0:
        return []

    result = []
    table = get_table()
    current = ""
    for char in text:
        total = current + chr(char)

        if total in table:
            current = total
        else:
            result.append(table[current])
            table[total] = len(table)
            current = chr(char)
            if len(table) == MAX_TABLE_SIZE:
                result.append(table[current])
                #result.append(table[CLEAR_CODE])
                table = get_table()
                current = ""

    result.append(table[current])
    #result.append(table[CLEAR_CODE])
    return pack(result)


def decompress(commpressed_data):
    if len(commpressed_data) == 0:
        return []

    # TODO: Check if compressing was not success.
    table = get_table2()
    prev = None
    result = ""
    for element in unpack(commpressed_data):
        if prev is None:
            if element not in table:
                raise Exception("Failed to decompress")
            prev = table[element]
            result += prev
            continue
        # if element == END_OF_DATA:
        #     raise Exception("Failed to decompress")
        # if element == CLEAR_CODE:
        #     table = get_table2()
        #     prev = None
        #     continue
        if element in table:
            string = table[element]
        elif element == len(table):
            string = prev + prev[0]
        else:
            raise Exception("Failed to decompress")

        result += string
        table[len(table)] = prev + string[0]
        if len(table) == MAX_TABLE_SIZE:
            table = get_table2()
        prev = string

    lst = list(map(ord, result))
    binary = struct.pack("B" * (len(result)), *lst)
    return binary


def to_bits(numb, count):
    temp = numb
    result = []
    while temp:
        result.append(temp % 2)
        temp = temp // 2
    while count - len(result) > 0:
        result.append(0)
    result.reverse()
    return result


def to_bytes(bits):
    result = []
    next_byte = 0
    next_bit = 7
    for bit in bits:
        if bit:
            next_byte = next_byte | (1 << next_bit)
        if next_bit:
            next_bit = next_bit - 1
            continue
        result.append(next_byte)
        next_bit = 7
        next_byte = 0
    if next_bit < 7:
        result.append(next_byte)
    return result


def get_min_width():
    min_width = 8
    while (1 << min_width) < TABLE_SIZE:
        min_width = min_width + 1
    return min_width


def pack(data):
    result = []
    tail = []
    current_size = TABLE_SIZE

    min_width = get_min_width()
    current_width = min_width

    for code in data:
        next_bits = to_bits(code, current_width)
        tail = tail + next_bits
        current_size = current_size + 1

        # if code == END_OF_DATA:
        #     for i in range((8 - (len(tail) % 8)) % 8):
        #         tail.append(0)
        # if code == CLEAR_CODE or code == END_OF_DATA:
        #     current_width = min_width
        #     current_size = TABLE_SIZE
        # elif 2 ** current_width <= current_size:
        if 2 ** current_width <= current_size:
            current_width = current_width + 1
        while len(tail) > 8:
            for byte in to_bytes(tail[:8]):
                result.append(byte)
            tail = tail[8:]
    for byte in to_bytes(tail):
        result.append(byte)
    return struct.pack("B" * (len(result)), *result)


def to_int(bits):
    result = 0
    for i in range(len(bits)):
        if bits[i] != 0:
            result += 1 << (len(bits) - i - 1)
    return result


def unpack(data):
    bits = []
    for value in struct.unpack("B" * (len(data)), data):
        for bit in to_bits(value, 8):
            bits.append(bit)

    result = []
    current_bits = []
    to_ignore_count = 0
    current_size = TABLE_SIZE

    min_width = get_min_width()
    current_width = min_width

    for i in range(len(bits)):
        if to_ignore_count > 0:
            to_ignore_count -= 1
            continue

        current_bits.append(bits[i])

        if len(current_bits) != current_width:
            continue

        code = to_int(current_bits)
        result.append(code)

        # if code == CLEAR_CODE or code == END_OF_DATA:
        #     current_size = TABLE_SIZE
        #     current_width = min_width
        # else:
        current_size = current_size + 1
        while 2 ** current_width <= current_size:
            current_width = current_width + 1

        # if code == END_OF_DATA:
        #     to_ignore_count = (8 - (i % 8)) % 8
        current_bits = []
    return result
