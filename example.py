from __future__ import print_function
from PIL import Image

"""the text 'hello' is embedded"""

im = Image.open('example1.jpg')
out = Image.open('output3.png')

inPix = im.load()
outPix = out.load()
li = []

for x in range(5471, 5471-11-14, -1):
    r, g, b = outPix[x, 3647]
    print(x)
    r = bin(r)[2:].zfill(8)
    g = bin(g)[2:].zfill(8)
    b = bin(b)[2:].zfill(8)

    r = r[-1]
    g = g[-1]
    b = b[-1]

    li.append(r)
    li.append(g)
    li.append(b)

li = ''.join(li)

print(li)