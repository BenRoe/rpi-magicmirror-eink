##
#  @filename   :   epd4in2b.py
#  @brief      :   Implements for Dual-color e-paper library
#  @author     :   Yehui from Waveshare
#
#  Copyright (C) Waveshare     August 15 2017
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
#

import RPi.GPIO as GPIO

import epdif

EPD_WIDTH = 400
EPD_HEIGHT = 300

# EPD4IN2B commands
PANEL_SETTING = 0x00
POWER_SETTING = 0x01
POWER_OFF = 0x02
POWER_OFF_SEQUENCE_SETTING = 0x03
POWER_ON = 0x04
POWER_ON_MEASURE = 0x05
BOOSTER_SOFT_START = 0x06
DEEP_SLEEP = 0x07
DATA_START_TRANSMISSION_1 = 0x10
DATA_STOP = 0x11
DISPLAY_REFRESH = 0x12
DATA_START_TRANSMISSION_2 = 0x13
VCOM_LUT = 0x20
W2W_LUT = 0x21
B2W_LUT = 0x22
W2B_LUT = 0x23
B2B_LUT = 0x24
PLL_CONTROL = 0x30
TEMPERATURE_SENSOR_CALIBRATION = 0x40
TEMPERATURE_SENSOR_SELECTION = 0x41
TEMPERATURE_SENSOR_WRITE = 0x42
TEMPERATURE_SENSOR_READ = 0x43
VCOM_AND_DATA_INTERVAL_SETTING = 0x50
LOW_POWER_DETECTION = 0x51
TCON_SETTING = 0x60
RESOLUTION_SETTING = 0x61
GSST_SETTING = 0x65
GET_STATUS = 0x71
AUTO_MEASURE_VCOM = 0x80
VCOM_VALUE = 0x81
VCM_DC_SETTING = 0x82
PARTIAL_WINDOW = 0x90
PARTIAL_IN = 0x91
PARTIAL_OUT = 0x92
PROGRAM_MODE = 0xA0
ACTIVE_PROGRAM = 0xA1
READ_OTP_DATA = 0xA2
POWER_SAVING = 0xE3


class EPD:
    def __init__(self):
        self.reset_pin = epdif.RST_PIN
        self.dc_pin = epdif.DC_PIN
        self.busy_pin = epdif.BUSY_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    def digital_write(self, pin, value):
        epdif.epd_digital_write(pin, value)

    def digital_read(self, pin):
        return epdif.epd_digital_read(pin)

    def delay_ms(self, delaytime):
        epdif.epd_delay_ms(delaytime)

    def send_command(self, command):
        self.digital_write(self.dc_pin, GPIO.LOW)
        # the parameter type is list but not int
        # so use [command] instead of command
        epdif.spi_transfer([command])

    def send_data(self, data):
        self.digital_write(self.dc_pin, GPIO.HIGH)
        # the parameter type is list but not int
        # so use [data] instead of data
        epdif.spi_transfer([data])

    def init(self):
        if (epdif.epd_init() != 0):
            return -1
        self.reset()
        self.send_command(BOOSTER_SOFT_START)
        self.send_data(0x17)
        self.send_data(0x17)
        self.send_data(0x17)  # 07 0f 17 1f 27 2F 37 2f
        self.send_command(POWER_ON)
        self.wait_until_idle()
        self.send_command(PANEL_SETTING)
        self.send_data(0x0F)  # LUT from OTP

    def wait_until_idle(self):
        while (self.digital_read(self.busy_pin) == 0):  # 0: busy, 1: idle
            self.delay_ms(100)

    def reset(self):
        self.digital_write(self.reset_pin, GPIO.LOW)  # module reset
        self.delay_ms(200)
        self.digital_write(self.reset_pin, GPIO.HIGH)
        self.delay_ms(200)

    def get_frame_buffer(self, image):
        buf = [0xFF] * int(self.width * self.height / 8)
        # Set buffer to value of Python Imaging Library image.
        # Image must be in mode 1.
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display. Expected:'
                             '({0}x{1}); actual: ({2}x{3}).'.format(self.width, self.height, imwidth, imheight))

        pixels = image_monocolor.load()
        for y in range(self.height):
            for x in range(self.width):
                # Set the bits for the column of pixels at the current position.
                if pixels[x, y] == 0:
                    buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        return buf

    def display_frame(self, frame_buffer_black, frame_buffer_red = None):
        if frame_buffer_black is not None:
            self.send_command(DATA_START_TRANSMISSION_1)
            self.delay_ms(2)
            for i in range(0, int(self.width * self.height / 8)):
                self.send_data(frame_buffer_black[i])
            self.delay_ms(2)
        if frame_buffer_red is not None:
            self.send_command(DATA_START_TRANSMISSION_2)
            self.delay_ms(2)
            for i in range(0, int(self.width * self.height / 8)):
                self.send_data(frame_buffer_red[i])
            self.delay_ms(2)

        self.send_command(DISPLAY_REFRESH)
        self.wait_until_idle()

    # after this, call epd.init() to awaken the module
    def sleep(self):
        self.send_command(VCOM_AND_DATA_INTERVAL_SETTING)
        self.send_data(0xF7)  # border floating
        self.send_command(POWER_OFF)
        self.wait_until_idle()
        self.send_command(DEEP_SLEEP)
        self.send_data(0xA5)  # check code
