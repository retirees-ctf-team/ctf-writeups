<p style="direction: rtl">
نگاه کلی:</br>
در کل این مسعله مربوط به الگوریتم های فشرده سازی و داشتن درک درست از فرآیند آنهاست، در این مسعله ما یک سروری داریم که فلگ داخل</br>
آن قرار دارد و ما میتوانیم <code>seed:string</code> را به سمت سرور ارسال کنیم تا سرور flag را با seed که از سمت ما فرستاده شده است را shuffle کند</br>
و سپس string مارو به ابتدای آن اضافه کند و بعد الگوریتم های مختلف فشرده سازی را روی آن انجام میدهد و اندازه خروجی هریک را به ما نشان میدهد</br>
الگوریتم های فشرده سازی با یکدیگر تفاوت خیلی زیادی دارند اما اگه بخوایم بصورت کلی بگیم این الگوریتم ها جلوی تکرار یه بایت و یا یک زنجیره ای از بایت ها</br>
رو میگیرند مثلا <code>AAAAAAAAAAAAAAAA</code> رو اگه بخوایم فشرده کنیم میتونیم به <code>A,16</code> تبدیلش کنیم که جلوی تکرارشو بگیریم حالا بریم سراغ حل مسعله.</br></br>
ما اگه فلگ رو توی سرور <code>DrgnS{ABCDEFGHIJKLMNOPQR}</code> در نظر بگیریم و seed رو 13 در نظر بگیریم shuffle شده فلگ توی سرور برابر <code>LGIREKHgADJFn}rMONSB{QPDC</code> خواهد بود</br>
حالا ما میخواهیم با اضافه کردن بایت های تکراری به اول عبارت shuffle شده رفتار الگوریتم های مختلف را برسی کنیم :</br>
</p>

```
# compression Input: gLGIREKHgADJFn}rMONSB{QPDC
13:g
    none   26
    zlib   34
   bzip2   67
    lzma   84

# compression Input: HLGIREKHgADJFn}rMONSB{QPDC
13:H
    none   26
    zlib   34
   bzip2   67
    lzma   84

# compression Input: LLGIREKHgADJFn}rMONSB{QPDC
13:L
    none   26
    zlib   34
   bzip2   67
    lzma   84
	
# compression Input: BLGIREKHgADJFn}rMONSB{QPDC
13:B
    none   26
    zlib   34
   bzip2   67
    lzma   84
```

<p style="direction: rtl">
خب حالا میام کد های سرور رو برسی میکنیم تا ببینیم چطور به این نتایج رسیده :</br>
</p>

```python
def none(v):
    return len(v)


def zlib(v):
    return len(codecs.encode(v, "zlib"))


def bzip2(v):
    return len(codecs.encode(v, "bz2"))


def lzma(v):
    return len(lz.compress(v))
```

<p style="direction: rtl">
از رو قسمت none که اندازه ورودی رو بدون فشرده سازی برمیگردونه میشه فهمید که سایز فلگ چند بوده مثلا برای وقتی که ورودی <code>13:g</code> هستش اندازه none 26 هستش پس میتوان نتیجه گرفت که فلگ 25 کاراکتری است.</br>
اما با فرستادن این چهار تا ورودی اندازه همه الگوریتم ها با هم برابر شده حتی با اینکه ما یه تکرار با وارد کردن <code>13:L</code> داشتیم و ورودی با <code>LL</code> شروع میشد، اما ممکنه که این الگوریتم ها 
با وجود تکرار های کم، تاثیری رو اندازه عبارت فشرده شده نذارن پس ما باید کاری کنیم که بتوانیم تکرار های بزرگتری ایجاد کنیم برای اینکار توی سرور اصلی از اونجایی که ما قسمت اول فلگ رو داریم و میدونیم که با</br>
<code>DrgnS</code> شروع میشه باید بدنبال یک seed باشیم که پس از shuffle کردن فلگ عبارت <code>DrgnS</code> ابتدای آن باشد برای اینکار میتوانیم seed ها را brute force کنیم.
</p>

```python
import random

# make 25 character flag
flag_format = b"DrgnS{" + b"A" * 18 + b"}"

seed = 0
while True:
    flag_copy = bytearray(flag_format)
    random.seed(seed)
    random.shuffle(flag_copy)
    if flag_copy.startswith(b'DrgnS'):
        print("Seed:", seed)
        print("Shuffled:", flag_copy)
    seed += 1

```

<p style="direction: rtl">خروجی: </p>

```
Seed: 2430447
Shuffled: bytearray(b'DrgnSAAAAAAAA{AAAA}AAAAAA')
Seed: 3723664
Shuffled: bytearray(b'DrgnS}AAAAAAAAAAAAAAAA{AA')
```

<p style="direction: rtl">
حالا میتوانیم تکرار هایی با طول بیشتر تولید کنیم، بریم یکبار دیگه برسی کنیم تا ببینیم با ایجاد تکرار های با طول بیشتر رفتار الگوریتم های مختلف و اندازه خروجی آنها چه تغییری خواهد کرد :</br>
</p>

```
# compression Input: DrgnSDrgnSGIECMRKL{BDOP}NAHFJQ

2430447:DrgnS
    none   30
    zlib   35
   bzip2   69
    lzma   88

# compression Input: AAAAADrgnSGIECMRKL{BDOP}NAHFJQ

2430447:AAAAA
    none   30
    zlib   36
   bzip2   70
    lzma   88

# compression Input: BBBBBDrgnSGIECMRKL{BDOP}NAHFJQ

2430447:BBBBB
    none   30
    zlib   36
   bzip2   70
    lzma   88

# compression Input: ABCDEDrgnSGIECMRKL{BDOP}NAHFJQ

2430447:ABCDE
    none   30
    zlib   38
   bzip2   69
    lzma   88

# compression Input: FGHIJDrgnSGIECMRKL{BDOP}NAHFJQ

2430447:FGHIJ
    none   30
    zlib   38
   bzip2   70
    lzma   88
```

<p style="direction: rtl">
اگه با دقت نگاه کنید توی الگوریتم lzma اندازه هیچ تغییری با دادن ورودی های مختلف نمیکنه پس معیار خوبی برای اینکه بتونیم بر اساس این تکرار ها فلگ رو بیرون بکشیم نخواهد بود اما در نقطه مقابل،</br>
zlib عبارت <code>DrgnS</code> که بیشترین تکرار رو بوجود آورده اندازه کمتری نسبت به بقیه ورودی ها دارد پس بیشترین مقدار فشرده سازی روی این ورودی انجام شده است، پس ما میتوانیم با بزرگ تر کردن</br>
طول تکرار و برسی اندازه zlib آن عبارت shuffle شده داخل سرور را بیابیم.
</p>

```python
from pwn import *
from string import ascii_uppercase

r = remote('localhost', 1337)

print(r.recvuntil(b'DrgnS{[A-Z]+}\n').decode())

seed = '2430447'
shuffled_flag = "DrgnS"

while len(shuffled_flag) < 25:
    min_zlib = 100000
    best_payload = ""
    for i in ascii_uppercase + '{}':
        payload = seed + ':' + shuffled_flag + i
        print(payload)
        r.sendline(payload.encode())
        r.recvuntil(b'zlib')
        zlib = int(r.recvline().decode().strip())
        r.recvline()
        if zlib < min_zlib:
            best_payload = i
            min_zlib = zlib
    shuffled_flag += best_payload

print("\nShuffled Flag: ", shuffled_flag)
```

<p style="direction: rtl">
خروجی :</br>
<code>DrgnSGIECMRAAAAAAAAAAAAAA</code></br>
خب اینجا تا قسمت <code>GIECMR</code> رو درست دراورده ولی از اینجا به بعد انگار بالا بردن تکرار توی اندازه ی خروجی الگوریتم zlib تاثیری نداشته دلیلش رو واضح نمیدونم ولی توی همچین موقعیت هایی میتونید بجای اینکه</br>
تک بایت تک بایت طول تکرار را زیاد کنید میتونید دوبایت دو بایت اینکار رو انجام بدید اما من اومدم همینکار رو روی seed دومی که بالاتر بدست اوردیم انجام دادم و خروجی زیر رو گرفتم :</br>
<code>Shuffled Flag:  DrgnS}EFLRKAGBMNQIHOCD{PJ</code>
برنامه ما اینجا درست کار کرده و تنها چیزی که باقی میمونه unshuffle کردن اونه که تقریبا کار راحتی و همون map کردن خودمونه :)</br>
کدش این میشه :</br>
</p>

```python
import random

random.seed(3723664)

shuffled = bytearray(b'DrgnS}EFLRKAGBMNQIHOCD{PJ')
flag = ['_' for _ in range(len(shuffled))]

mapp = [i for i in range(len(shuffled))]
random.shuffle(mapp)

for i in range(len(mapp)):
    flag[mapp[i]] = chr(shuffled[i])

print("".join(flag))

```

<p style="direction: rtl">
خروجی:</br>
<code>DrgnS{ABCDEFGHIJKLMNOPQR}</code></br></br>
که همون فلگی هستش که ما توی سرور local خودمون ست کرده بودیم و حالا اگه همین برنامه روی سرور اصلی اجرا کنید فلگ رو بهتون میده که فلگ اصلی :</br>
<code>DrgnS{THISISACRIMEIGUESS}</code></br></br>

</p>