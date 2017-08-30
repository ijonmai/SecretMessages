# Program: Text In Image Project
#    Name: Jon Mai
#    CWID: 893951798
#   Class: CPSC 353
#    Date: April 6, 2017

# Description
Program is divided into a couple functions but main ones are changeBits and exTex.

Function changeBits does what it sounds like it does. Takes in the pixels and the binary string to embed and returns the changed pixels to the image and saves it.

Function exTex takes in the pixels of the image and the text length extracted from the first 11 pixels and begins extracting the LSB until it hits the amount of bits from text length.

# Execution
To encrypt:
python textInImage.py  -e image_path.jpg -o output_file.png -t "text goes here"

To decrypt:
python textInImage.py -d output_file.png