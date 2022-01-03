import string

mem = []
exec('mem = ' + open('memoryDump.txt', 'r').read())


def rol(x, val):
    return ((x << val) + (((val << 15) & x) >> 15)) & 0xffff


def pad_hex(number: int, pad: int) -> str:
    return "{0:#0{1}x}".format(number, pad + 2)


def read_word(offset: int) -> int:
    return int('0x' + mem[offset + 1] + mem[offset], 16)


def write_word(inp: int, offset: int):
    what_to_write = pad_hex(inp, 4)[2:]
    mem[offset + 1] = what_to_write[:2]
    mem[offset] = what_to_write[2:]


password_Input = string.ascii_uppercase[:26]
input_index = 0

while read_word(0) != 0xFFFF:

    EAX = 1

    if read_word(8) == 1:
        write_word(0, 8)
        print(chr(read_word(6)), end='')
        # print('\nmem[0x%x]  -------> printf("%s")' % (6, chr(read_word(6))))

    if read_word(12) == 1:
        write_word(0, 12)
        write_word(ord(password_Input[input_index]), 10)
        # print('\ngetChar("%s") -------> mem[0x%x]' % (process_Input[input_index], 10))
        input_index += 1

    EAX = read_word(0)
    ECX = read_word(EAX * 2 + 2)
    ESI = read_word(EAX * 2)
    EDI = read_word(EAX * 2 + 4)

    EAX += 3
    write_word(EAX, 0)
    value = ~(read_word(ECX * 2) | read_word(ESI * 2)) & 0xffff
    # print('\n~(0x%x | 0x%x) == 0x%x -------> mem[0x%x]' % (read_word(ECX * 2), read_word(ESI * 2), value, EDI * 2))
    write_word(value, EDI * 2)
    write_word(rol(value, 1), 2)
