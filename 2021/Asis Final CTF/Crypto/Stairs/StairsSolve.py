# Encryption Function:
# -------------------------------------------
# def encrypt(m, pubkey):
#     e, n = 5, pubkey
#     M = bytes_to_long(flag)
#     m += M
#     c = (pow(m, e, n) + m) % n
#     return c
# -------------------------------------------

import socket
import time
import sympy as sym
from Crypto.Util.number import long_to_bytes


def rec_data():
    result = b''
    try:
        data = s.recv(1024)
        while data:
            result += data
            data = s.recv(1024)
    except:
        pass
    return result


def send_data(data):
    s.send(data + b'\n')
    time.sleep(1)


e = 5

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('95.217.210.96', 11010))
s.settimeout(1)

print(rec_data().decode())
send_data(b'P')
pubkey = int(rec_data().decode().lstrip('pubkey = '))
print('pubkey = ', pubkey)


flag = sym.Symbol('flag')
eqa = {}
for counter in range(-1, 2):
    send_data(b'T')
    rec_data()
    send_data(str(counter).encode())
    print(counter)
    enc = int(rec_data().decode().lstrip('| the encrypted message is: '))
    print('| the encrypted message is: ', enc)
    eqa[counter] = enc

final_flag = int(sym.solve(20*flag**3 + 10*flag - (eqa[1] + eqa[-1] - 2 * eqa[0]))[0])
print(long_to_bytes(final_flag))
