#!/usr/bin/python3
"""
Set of functions to encode/decode ASCII text into image.
Max 255 characters length message allowed at a time,
but easily upgradable for more.
"""
import argparse

from collections import deque

from PIL import Image
import PIL.Image


class LoadingDone(Exception):
    """Exception to refer done of loading bits."""


def make_8bit(string):
    if len(string) < 8:
        return "0" * (8 - len(string)) + string
    else:
        return string


def split_by_two(string):
    return [string[i:i+2] 
            for i in range(0, len(string), 2)]


def encode(message, in_img, out_img="coded.png"):
    print("Encoding ({}): {}".format(len(message), message))

    if len(message) > 255:
        print("Too big message. Max. 255 characters allowed.")
        return -1

    length = make_8bit(bin(sum(len(s) for s in message))[2:])
    message = deque(make_8bit(bin(ord(ch))[2:])
               for ch in message)

    bits = deque(split_by_two(length))
    for mes in message:
        bits.extend(split_by_two(mes))

    image = Image.open('tests/to_encode.jpg').convert("RGBA")
    try:
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                pixs = [bin(pix)[2:] for pix in image.getpixel((x, y))]
                pixs = tuple(int(pix[:len(pix)-2] + bits.popleft(), 2) 
                        for pix in pixs)

                image.putpixel((x, y), pixs)
    except IndexError:
        print("Finished:", out_img)

    return image


def decode(img):
    print("Decoding:", img)

    bits = []
    length = None
    image = Image.open(img)
    try:
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                pixs = [bin(pix)[2:] for pix in image.getpixel((x, y))]
                pixs = tuple(pix[len(pix)-2:]
                             for pix in pixs)

                bits.extend(pixs)

                if not length and len(bits) > 3:
                    length = int("".join(x for x in bits[:4]), 2)

                if len(bits) == (length * 4 + 4):
                    raise LoadingDone
    except LoadingDone:
        pass

    bits = bits[4:]
    chars = []
    for i in range(0, len(bits), 4):
        chars.append("".join(x for x in bits[i:i+4]))

    message = "".join(chr(int(ch, 2)) for ch in chars)

    print("Length:", length)
    print("Message:", message)

    return message
    
    


