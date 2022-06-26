#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Code shamelessly taken from the pimoroni repository, thank you Sandy Macdonald:
https://github.com/pimoroni/bmp280-python/blob/master/examples/temperature-and-pressure.py
and
Richard Hull (and contributors)
https://github.com/rm-hull/luma.examples/blob/master/examples/clock.py
"""
import datetime
import time
import sys
from luma.core import cmdline
from luma.core.render import canvas
from bmp280 import BMP280
from PIL import ImageFont

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

emoji = "¯\_(ツ)_/¯"
platform = "@github"
author = "promethee"

FontTemp = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 92)
FontTemp2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 32)
FontDate = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
FontDebug = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
FontEmoji = ImageFont.truetype('./CODE2000.TTF', 22)

offset = sys.argv[1] if len(sys.argv) > 1 else 0

last_temperature = 0

def init_bmp280():
    bus = SMBus(1)
    bmp280 = BMP280(i2c_dev=bus)
    return bmp280

def init_oled():
    parser = cmdline.create_parser(description='luma.examples arguments')
    config = cmdline.load_config('./ssh1107.pimoroni.conf')
    args = parser.parse_args(config + [])
    device = cmdline.create_device(args)
    return device

def main(bmp280, device):
    global last_temperature
    while True:
        time.sleep(1)
        now = datetime.datetime.now()
        datetimestamp = now.strftime("%Y/%m/%d @ %H:%M:%S")
        temperature = '{:d}'.format(int(bmp280.get_temperature() - float(offset)))

        try:
            if temperature != last_temperature:
                last_temperature = temperature

            with canvas(device) as draw:
                print(datetimestamp, temperature, '°C')
                draw.text((0, 0), temperature, fill="white", font=FontTemp)
                draw.text((48, 92), '°C', fill="white", font=FontTemp2)
        except Error as e:
            print(datetimestamp, 'bmp280 has been removed or is missing', e)
            bmp280 = init_bmp280()
            device = init_oled()
            with canvas(device) as draw:
                error_message = 'bmp280 \nhas been \nremoved \nor is missing'
                draw.text((0, 0), error_message, fill="white", font=FontDebug)

if __name__ == "__main__":
    try:
        bmp280 = init_bmp280()
        device = init_oled()
        with canvas(device) as draw:
            draw.text((16, 12), emoji, fill="white", font=FontEmoji)
            draw.text((16, 54), platform, fill="white", font=FontDate)
            draw.text((8, 96), author, fill="white", font=FontDate)
        time.sleep(3)
        main(bmp280, device)
    except KeyboardInterrupt:
        pass
