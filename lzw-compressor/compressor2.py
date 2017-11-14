import struct


#CLEAR_CODE = 256
#END_OF_DATA = 257
END_OF_BLOCK = 256
TABLE_SIZE = 257
MAX_TABLE_SIZE = 2 ** 32


def get_table():
    table = {}
    for i in range(256):
        table[chr(i)] = i
    #table[CLEAR_CODE] = CLEAR_CODE
    #table[END_OF_DATA] = END_OF_DATA
    table[END_OF_BLOCK] = END_OF_BLOCK
    return table


def get_table2():
    table = {}
    for i in range(256):
        table[i] = chr(i)
    #table[CLEAR_CODE] = CLEAR_CODE
    #table[END_OF_DATA] = END_OF_DATA
    table[END_OF_BLOCK] = END_OF_BLOCK
    return table


def compress(bytes):
    # TODO: Set flag if compressing was success.
    bytes = struct.unpack("B" * len(bytes), bytes)
    result = encode(bytes)
    if (len(result) > len(bytes)):
        result = bytearray([0]) + bytes
    return pack(result)


def encode(bytes, result=[]):
    text = struct.unpack("B" * len(bytes), bytes)
    if len(text) == 0:
        return []

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
    return result


def add_split_code(result):
    result.append(END_OF_BLOCK)
    return result


def decompress(compressed_data):
    # TODO: Check if compressing was not success.
    if len(compressed_data) == 0:
        return []
    result = []
    bytes = unpack(compressed_data)
    offset = 0
    while offset != len(bytes):
        offset, name = decode(bytes, offset)
        offset, content = decode(bytes, offset)
        content_bytes = str_to_bytes(content)
        result.append((name, content_bytes))
    return result



def str_to_bytes(str):
    lst = list(map(ord, str))
    binary = struct.pack("B" * (len(str)), *lst)
    return binary


def decode(data, offset):
    table = get_table2()
    prev = None
    result = ""
    finish = len(data)
    for i in range(offset, len(data)):
        element = data[i]
        if prev is None:
            if element not in table:
                raise Exception("Failed to decompress")
            prev = table[element]
            result += prev
            continue
        if element == END_OF_BLOCK:
            finish = i + 1
            break
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
    return finish, result


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
