# Program: Text In Image Project
#    Name: Jon Mai
#    CWID: 893951798
#   Class: CPSC 353
#    Date: April 6, 2017

from __future__ import print_function
from PIL import Image
import argparse
import sys

# Function to show how many bits there are in a string
def bitsInString(str):
    return 8 * len(str)


# Function converts amount of bits to binary with leading zeroes
def numOfBitsTo32Bits(numOfBits):
    numOfBits = bin(numOfBits)[2:].zfill(32)
    return numOfBits


def numOfBitsTo8Bits(numOfBits):
    numOfBits = bin(numOfBits)[2:].zfill(8)
    return numOfBits


def changeBits(pixels, li, position):
    # Put all pixel data into a list for easier access
    pixels = list(pixels)
    i = len(pixels) - position - 1

    # While loop takes the string li and changes the pixel's LSB according to li[0], then pops until li is empty
    while li:
        r, g, b = pixels[i]
        # change last bit of r, g, b to what is in
        r = bin(r)[2:].zfill(8)
        r = list(r)
        r[7] = li[0]
        li.pop(0)

        # exit while loop once li is empty in case r value does not need to obtain anything
        if not li:
            r = ''.join(r)
            r = int(r, 2)
            pixels[i] = r, g, b
            return pixels
            break

        g = bin(g)[2:].zfill(8)
        g = list(g)
        g[7] = li[0]
        li.pop(0)

        # exit while loop once li is empty because b value will not obtain anything
        if not li:
            r = ''.join(r)
            g = ''.join(g)
            r = int(r, 2)
            g = int(g, 2)
            pixels[i] = r, g, b
            return pixels
            break

        b = bin(b)[2:].zfill(8)
        b = list(b)
        b[7] = li[0]
        li.pop(0)
        # turns list back into full string
        r = ''.join(r)
        g = ''.join(g)
        b = ''.join(b)

        # converts the binary string into a decimal and sets it equal to r, g, and b, thus changing the pixel value
        r = int(r, 2)
        g = int(g, 2)
        b = int(b, 2)
        pixels[i] = r, g, b
        i -= 1
    return pixels


# extract Text Length
def exTextLen(pixels):
    pixels = list(pixels)
    x = len(pixels)
    li = []
    # Goes through pixel 0-10 and converts into binary with leading 0s
    for x in range(x - 1, x - 12, -1):
        r, g, b = pixels[x]
        r = bin(r)[2:].zfill(8)
        g = bin(g)[2:].zfill(8)
        b = bin(b)[2:].zfill(8)

        # set value equal to the LSB then appends it into a list
        r = r[-1]
        g = g[-1]
        b = b[-1]
        li.append(r)
        li.append(g)
        li.append(b)

    # this gets rid of the last bit because it is an extra
    li = li[:-1]

    # Joins the list into a single string
    # Now we have a binary value we can use to convert into decimal
    li = ''.join(li)
    textLength = int(li, 2)
    return textLength


# extract text
def exText(pixels, textLength, position):
    # This portion of the code takes the RGB decimal values, turns it into binary, and adds it to a list
    pixels = list(pixels)
    li = []
    x = len(pixels) - 1
    for x in range(len(pixels) - position - 1, len(pixels) - position - textLength, -1):
        r, g, b = pixels[x]
        r = bin(r)[2:].zfill(8)
        g = bin(g)[2:].zfill(8)
        b = bin(b)[2:].zfill(8)

        r = r[-1]
        g = g[-1]
        b = b[-1]

        li.append(r)
        li.append(g)
        li.append(b)
    # turn list into a full string
    li = ''.join(li)

    # initialize message list
    message = []
    # begin extracting text
    while textLength:
        # sets text equal to the first 8 characters in string 'li'
        text = li[:8]
        # turns the binary value of text into a decimal
        text = int(text, 2)
        # turns the decimal into an ascii
        text = chr(text)
        # gets rid of the 8 bits we just read
        li = li[8:]

        # add the text character into a list
        message.append(text)
        textLength -= 8

    # turn the list into a full string to read easier
    message = ''.join(message)
    print(message)


def main(image_path, output_file, text, should_encrypt):
    image = Image.open(image_path)
    pixel = image.getdata()
    width, height = image.size
    str = text

    # encryption
    if should_encrypt:
        # this is the encrypt portion
        bitLength = bitsInString(str)

        # This determines whether program will move forward or not
        # If the image is not large enough for the text to be embedded
        # it will exit the program

        bitLen = numOfBitsTo32Bits(bitLength)
        bitLen = list(bitLen)
        # First 11 pixels
        position = 0
        pixel = changeBits(pixel, bitLen, position)

        # Embed rest of characters
        position = 11
        str = list(str)
        strList = []
        while str:
            temp = ord(str[0])
            temp = numOfBitsTo8Bits((temp))
            temp = list(temp)
            strList.append(temp)
            str.pop(0)
        # flatten list so there aren't lists within list
        strList = sum(strList, [])
        pixel = changeBits(pixel, strList, position)
        image.putdata(pixel)
        image.save(output_file, 'PNG')

    # decryption
    else:
        textLength = exTextLen(pixel)
        position = 11
        exText(pixel, textLength, position)


if __name__ == '__main__':
    # Reference for argparse
    # Tutorial watched: https://youtu.be/rnatu3xxVQE
    # May look similar to Reza Nikoopour as well

    parser = argparse.ArgumentParser(description='This program hides text inside an image.')

    # Some optional arguments
    # These are mutually exclusive, not allowed to run with each other
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', action='store_true', help = 'This starts the encryption', default=False)
    group.add_argument('-d', '--decrypt', action='store_true', help = 'This starts the decryption', default=False)

    # This is the positional argument
    parser.add_argument('image_path', help='Image you wish to hide text in')

    # Additional optional arguments
    parser.add_argument('-t', '--text', help='Text you wish to hide')
    parser.add_argument('-o', '--output_file', help='Name of the output image', default=None)
    args = parser.parse_args()
    image = Image.open(args.image_path)
    width, height = image.size
    size = width*height

    if args.encrypt and len(args.text)*8 > size:
        sys.exit('Image too small to encrypt your text')
    if args.encrypt and not args.text and not args.output_file:
        sys.exit('Text is required to encrypt into image')


    main(args.image_path, args.output_file, args.text, args.encrypt)