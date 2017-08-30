import argparse
import sys
import re
import itertools

from PIL import Image

# start from bottom right to top left



def stringBits(string):
    return len(string) * 8


def convertTo8Bits(bitString):
    #fill in entire byte
    bitString = bin(bitString)[2:].zfill(8)
    return bitString


def convertTo32Bits(bitString):
    # fill in the entire byte
    bits = bin(bitString)[2:].zfill(32)
    return bits

def leastSignificantBit(byte, bit):
    # take the least significant bit
    bitFormat = list(format(byte, 'b'))
    bitFormat[-1] = bit
    bitFormat = ''.join(bitFormat)
    return bitFormat


def extractLastBit(byte):
    # take the last bit
    bitFormat = list(format(byte, 'b'))
    return bitFormat[-1]


def decodeImage(bits, data, index=0):
    bitString = ''
    position = index + bits
    # index through red, green, and blue for their data
    while index <= position:
        red = data[index]
        green = data[index]
        blue = data[index]
        index += 1
        # as the while loop goes through, append to the bitstring from each red, green, blue bit
        bitString += extractLastBit(red)
        bitString += extractLastBit(green)
        bitString += extractLastBit(blue)
    return bitString[:bits]


#def extractLength(data):
    #binaryLength = decodeImage(int_size, data, startOfTextLength)
    #length = int(binaryLength, 2)
    #return length


def extractText(data, bits):
    binaryString = decodeImage(data, bits, maxSize)
    letters = re.findall('........', binaryString)
    text = ''
    # convert back from binary into text
    for letter in letters:
        value = int(letter, 2)
        text += chr(value)
    return text


#def extractHiddenText(data):
    #bits = extractLength(data)
    #text = extractText(data, bits)
    #print(text)

def encryption(pixels, str, startPosition):
	# create list to begin encryption
    strList = list(str)
    pixels = list(pixels)
    x = len(pixels)-startPosition-1
	# loop through the red, green, blue values to convert them into 8 bits
    while strList:
        r, g, b = pixels[x]
        r = convertTo8Bits((r))
        g = convertTo8Bits((g))
        b = convertTo8Bits((b))

		# 
        r = r[:-1] + strList[0]
        strList.pop(0)
        if not strList:
            r = int(r, 2)
            g = int(g, 2)
            b = int(b, 2)
            pixels[x] = r, g, b
            return pixels
            break

        g = g[:-1] + strList[0]
        strList.pop(0)
        if not strList:
            r = int(r, 2)
            g = int(g, 2)
            b = int(b, 2)
            pixels[x] = r, g, b
            return pixels
            break

        b = b[:-1] + strList[0]
        strList.pop(0)

        r = int(r, 2)
        g = int(g, 2)
        b = int(b, 2)
        pixels[x] = r, g, b
        x -= 1
    return pixels

def stringToBinary(string):
	# create list to store the binary value
    list(string)
    bitArray = []
	# go through the string to convert into bits and join them together
    for x in range(0, len(string)):
        letter = string[x]
        bits = convertTo8Bits(ord(letter))
        bits = list(bits)
        bitArray.append(bits)
    bitArray = list(itertools.chain(*bitArray))
    bitArray = ''.join(bitArray)
    return bitArray

def main(image_path, output_file, text, should_encrypt):
    
	
	img = Image.open(image_path)
	pixels = img.getdata()
	width, height = img.size
	maxSize = width*height
	startOfText = 11
	int_size = 32
	str = text
	
	if should_encrypt:	
	# embed text length in first 11 pixels
		startPosition = 0
		string32bits = convertTo32Bits((stringBits(str)))
		pixel = encryption(pixels, string32bits, startPosition)
		img.putdata(pixel)

    # embed text into pixels after the first 11
		startPosition=11
		pixel = encryption(pixels, stringToBinary(str), startPosition)
		img.putdata(pixel)
		img.save(outputFile, 'PNG')
	else:
		print()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-e', '--encrypt', action='store_true', default=False)
	group.add_argument('-d', '--decrypt', action='store_true', default=False)

	parser.add_argument('image_path', help='Name of image to hide text in')

	parser.add_argument('-o', '--output_file', help='Name of output file.png', action='None')
	parser.add_argument('-t', '--text', help='Your secret message')

	args=parser.parse_args()

	if args.encrypt and not args.text and not args.output:
		print('Text required to encrypt message')
		sys.exit(0)

	main(args.image_path, args.output_file, args.text, args.encrypt)
