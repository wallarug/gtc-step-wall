# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
NeoPixel example for Pico. Turns the NeoPixels red.

REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP0.
"""
import board
import neopixel
import random
import time

n_leds = 288
num_pixels = n_leds
pixels = neopixel.NeoPixel(board.GP0, num_pixels, auto_write=False)
pixels.brightness = 1.0


print("Starting")
# Set the pixels to OFF to start
pixels.fill((0,0,0))
pixels.show()

time.sleep(2)

def fire_animation():
    while True:
        rgb = (255, 42, 12)  # (255, 96, 12)
        delay = random.choice(range(25, 100))/1000  #50, 150

        for p in range(n_leds):
            flicker = random.choice(range(40))
            rgb_r = tuple([x - flicker if x-flicker >= 0 else 0 for x in rgb ])
            pixels[p] = rgb_r
        pixels.show()
        time.sleep(delay)

fire_animation()
