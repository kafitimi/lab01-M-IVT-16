# -*- coding: utf-8 -*-
import sys, struct
from math import ceil

filename = sys.argv[1] if len(sys.argv)>1 else "gray3x3.txt"
lines = open(filename).readlines()
N, M, color = map(int, lines[0].split())
r, g, b = [], [], []

# rows - список строк *в порядке снизу вверх*, каждая строка - список целых чисел. 
# Если изображение полноцветное ширины, например, 100, то каждая строка содержит 300 чисел,
# из которых первые три - это компоненты R, G, B пикселя в верхнем левом углу
rows = [list(map(int, line.split())) for line in lines[-1:0:-1]]

for i in rows:
        if color:
                while (len(rows[0]) % 4 != 0) or (len(rows[0]) % 3 != 0) :
                        for j in range (0,M):
                                rows[j].append(0)
                r.extend(i[0::3])
                g.extend(i[1::3])
                b.extend(i[2::3])
        else:
                b.extend(i)

        
BMFheader = BMIheader = palette = b''

size = 54 + N*3*4
bitperpixel = 24 if color else 8
if color:
        pixelstart=54
else:
        pixelstart=54+256*4
BMFheader = struct.pack('<2sihhi', b'BM', size, 0, 0, pixelstart)
BMIheader = struct.pack('<iiihhiiiiii', 40, N, M, 1, bitperpixel, 0, 0, 0, 0, 0, 0)

if color:
        pixeldata = b''.join([struct.pack('BBB', b[i],g[i],r[i]) for i in range(len(rows[0]))])
else:
	palette = b''.join([struct.pack('BBBB', i,i,i,0) for i in range(256)])
	pixeldata = b''.join([struct.pack('<i', palette.index(i)) for i in b])

open(filename+".bmp","wb").write(BMFheader + BMIheader + palette + pixeldata)
