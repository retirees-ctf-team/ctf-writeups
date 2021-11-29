import socket
import os
from Crypto.Cipher import AES


def split_by(data, cnt):
    return [data[i: i + cnt] for i in range(0, len(data), cnt)]


def pad(data, bsize):
    b = bsize - len(data) % bsize
    return data + bytes([b] * b)


def xor(a, b):
    return bytes(aa ^ bb for aa, bb in zip(a, b))


def sign(data, key):
    data = pad(data, 16)
    blocks = split_by(data, 16)
    mac = b'\0' * 16
    aes = AES.new(key, AES.MODE_ECB)
    for block in blocks:
        mac = xor(mac, block)
        mac = aes.encrypt(mac)
    mac = aes.encrypt(mac)
    return mac


def verify(data, key):
    if len(data) < 16:
        return False, ''
    tag, data = data[:16], data[16:]
    correct_tag = sign(data, key)
    if tag != correct_tag:
        return False, ''
    return True, data


def main():
    global c, key

    while True:
        c.send(b'What to do?\n')
        c.send(b'> ')
        opt = c.recv(1024).decode().strip()
        if opt == 'sign':
            c.send(b'> ')
            data = c.recv(1024).decode().strip()
            data = bytes.fromhex(data)
            if b'gimme flag' in data:
                c.send(b'That\'s not gonna happen\n')
                break
            c.send((sign(data, key) + data).hex().encode() + b'\n')
        elif opt == 'verify':
            c.send(b'> ')
            data = c.recv(1024).decode().strip()
            data = bytes.fromhex(data)
            ok, data = verify(data, key)
            if ok:
                if b'gimme flag' in data:
                    with open('flag.txt', 'rb') as f:
                        c.send(f.read())
                else:
                    c.send(b'looks ok!\n')
            else:
                c.send(b'hacker detected!\n')
        else:
            c.send(b'??\n')
            break
    return 0


if __name__ == '__main__':
    key = os.urandom(16)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 1234))
    s.listen(1)
    c, a = s.accept()
    exit(main())
