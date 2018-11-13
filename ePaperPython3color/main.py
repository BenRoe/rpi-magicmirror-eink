#!/usr/bin/python

##
 #  @filename   :   main.cpp
 #  @brief      :   7.5inch e-paper display demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 28 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import epd7in5b
import Image
import ImageDraw
import ImageFont
#import imagedata

EPD_WIDTH = 640
EPD_HEIGHT = 384

def main():
    epd = epd7in5b.EPD()
    epd.init()

    # For simplicity, the arguments are explicit numerical coordinates
    # image_red = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the frame
    # draw_red = ImageDraw.Draw(image_red)
    # image_black = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the frame
    # draw_black = ImageDraw.Draw(image_black)
    # font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)
    # draw_red.rectangle((0, 6, 640, 40), fill = 0)
    # draw_red.text((200, 10), 'e-Paper demo', font = font, fill = 255)
    # draw_red.rectangle((200, 80, 600, 280), fill = 0)
    # draw_red.chord((240, 120, 580, 220), 0, 360, fill = 255)
    # draw_black.rectangle((20, 80, 160, 280), fill = 0)
    # draw_red.chord((40, 80, 180, 220), 0, 360, fill = 0)
    # epd.display_frame(epd.get_frame_buffer(image_black),epd.get_frame_buffer(image_red))

    # display images
    frame_black = epd.get_frame_buffer(Image.open('black.png'))
    frame_red = epd.get_frame_buffer(Image.open('white.png'))
    epd.display_frame(frame_black, frame_red)


if __name__ == '__main__':
    main()
