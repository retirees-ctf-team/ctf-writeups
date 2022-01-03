import string

mem = []
exec('mem = ' + open('memoryDump.txt', 'r').read())


def rol(x, val):
    return ((x << val) + (((val << 15) & x) >> 15)) & 0xffff


def pad_hex(number: int, pad: int) -> str:
    return "{0:#0{1}x}".format(number, pad + 2)


def read_word(memIn: list, offset: int) -> int:
    return int('0x' + memIn[offset + 1] + memIn[offset], 16)


def write_word(memIn: list, inp: int, offset: int):
    what_to_write = pad_hex(inp, 4)[2:]
    memIn[offset + 1] = what_to_write[:2]
    memIn[offset] = what_to_write[2:]


def correct_characters(inp):
    mem_copy = mem.copy()
    input_index = 0
    correct_counter = 0
    while read_word(mem_copy, 0) != 0xFFFF:

        if read_word(mem_copy, 8) == 1:
            write_word(mem_copy, 0, 8)
            # print(chr(read_word(6)), end='')

        if read_word(mem_copy, 12) == 1:
            write_word(mem_copy, 0, 12)
            write_word(mem_copy, ord(inp[input_index]), 10)
            input_index += 1

        EAX = read_word(mem_copy, 0)
        ECX = read_word(mem_copy, EAX * 2 + 2)
        ESI = read_word(mem_copy, EAX * 2)
        EDI = read_word(mem_copy, EAX * 2 + 4)

        EAX += 3
        write_word(mem_copy, EAX, 0)
        value = ~(read_word(mem_copy, ECX * 2) | read_word(mem_copy, ESI * 2)) & 0xffff
        if EDI * 2 == 0x3dc and value == 0:
            correct_counter += 1
        write_word(mem_copy, value, EDI * 2)
        write_word(mem_copy, rol(value, 1), 2)
    return correct_counter


possible_characters = list(string.printable)
for toxic_character in [':', '<', '>']:
    possible_characters.remove(toxic_character)

password = ''
process_Input = list(string.ascii_uppercase[:26])
for i in range(26):
    for char in possible_characters:
        process_Input[i] = char
        if correct_characters(''.join(process_Input)) > len(password):
            password += char
            break
    print(password)
print("Password: ", password)
