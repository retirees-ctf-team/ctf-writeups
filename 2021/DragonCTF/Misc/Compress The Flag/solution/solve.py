#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Filename:         solve.py
# Author:           Mahdi Heidari
# Task:             Compress The Flag
# Competition:      Dragon CTF 2021
# Category:         Miscellaneous
# Scoring:          156 pts (easy)
# Number of solves: 75 out of 247 teams

from pwn import *
import string
import re

#context.log_level = 'debug'

def DetectSeed():
    FLAG = b"DrgnS{ABCEFGHIJKLMNOPQRX}" # from none we know falg length=25
    MySeed = {}
    for i in range(150):
        flag = bytearray(FLAG)
        random.seed(i)
        random.shuffle(flag)
        k = FLAG.index(flag[0])
        if k not in MySeed :
            MySeed[k] = i
    return MySeed

def Guess(conn, MySeed):
    MyStr = "DrgnS{"
    for key in sorted(MySeed):
        index , seed = key, MySeed[key]
        if index<6 or index==24:
            continue
        
        for ch in reversed(string.ascii_uppercase):
            test_string =  ch.encode() * 9 

            conn.sendline( f"{seed}:{test_string.decode()}".encode() )
            
            noneo = int(re.search(r'\d+$', conn.recvline().decode()).group())
            zlibo = int(re.search(r'\d+$', conn.recvline().decode()).group())
            bzip2o = int(re.search(r'\d+$', conn.recvline().decode()).group())
            lzmao = int(re.search(r'\d+$', conn.recvline().decode()).group())
            conn.recvline()

            if zlibo<=35 :
                MyStr += ch
                print(f"find index {index:>2} = {ch}")
                break
                
    MyStr += "}"
    return MyStr

def main():
    conn = remote("compresstheflag.hackable.software", 1337)
    conn.recvuntil(b"DrgnS{[A-Z]+}\n")

    MySeed = DetectSeed()

    flag = Guess(conn, MySeed)

    print(f"flag = {flag}")   # DrgnS{THISISACRIMEIGUESS}


if __name__ == "__main__":
    main()