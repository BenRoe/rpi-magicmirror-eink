import argparse

import epd7in5
import epd4in2b

from PIL import Image
import PIL.ImageOps


def invert(image):
    if image.mode == 'RGBA':
        r,g,b,a = image.split()
        rgb_image = Image.merge('RGB', (r,g,b))
        inverted_image = PIL.ImageOps.invert(rgb_image)
        r2,g2,b2 = inverted_image.split()
        return Image.merge('RGBA', (r2,g2,b2,a))
    else:
        return PIL.ImageOps.invert(image)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("screen")
    parser.add_argument("--invert", help="invert screen", action="store_true")
    args = parser.parse_args()
    if args.screen == "epd7in5":
        imagecount = 1
        epd = epd7in5.EPD()
    elif args.screen == "epd4in2b":
        imagecount = 2
        epd = epd4in2b.EPD()
    else:
         raise Exception("Unsupported screen, please submit a code patch")
    epd.init()

    image = Image.open('black.png')
    if args.invert:
        image = invert(image)

    if imagecount == 1:
       epd.display_frame(epd.get_frame_buffer(image))
    elif imagecount == 2:
       epd.display_frame(epd.get_frame_buffer(image), epd.get_frame_buffer(image))

if __name__ == '__main__':
    main()
