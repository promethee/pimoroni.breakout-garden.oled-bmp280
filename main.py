#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Code shamelessly taken from the pimoroni repository, thank you Sandy Macdonald:
https://github.com/pimoroni/bmp280-python/blob/master/examples/temperature-and-pressure.py
and
Richard Hull (and contributors)
https://github.com/rm-hull/luma.examples/blob/master/examples/clock.py
"""
import time
import datetime
import sys
from luma.core import cmdline
from luma.core.render import canvas
from bmp280 import BMP280
from PIL import ImageFont

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

def main():
    bus = SMBus(1)
    bmp280 = BMP280(i2c_dev=bus)

    actual_args = sys.argv[1:]
    parser = cmdline.create_parser(description='luma.examples arguments')
    config = cmdline.load_config('./sh1107.pimoroni.conf')
    args = parser.parse_args(config + actual_args)
    device = cmdline.create_device(args)
    FontTemp = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
    FontDate = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
    FontTime = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28)

    offset = 12

    while True:
        with canvas(device) as draw:
            now = datetime.datetime.now()
            today_date = now.strftime("%Y/%m/%d")
            today_time = now.strftime("%H:%M:%S")
            temperature = '{:d}°C'.format(int(bmp280.get_temperature() - offset))

            draw.text((0, 0), temperature, fill="white", font=FontTemp)
            draw.text((0, 60), today_date, fill="white", font=FontDate)
            draw.text((0, 92), today_time, fill="white", font=FontTime)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
