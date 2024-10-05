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

n_leds = 144 #432
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
        rgb = (255, 72, 12)  # (255, 96, 12)
        blue_rgb = (0, 0, 0)  # Blue color
        
        delay = random.choice(range(50, 150))/1000  #50, 150

        for p in range(0, n_leds, 3):
            flicker = random.choice(range(40))

            # 5% chance to turn the LED blue instead of flickering red
            if random.random() < 0.5:
                rgb_r = blue_rgb
            else:
                rgb_r = tuple([x - flicker if x-flicker >= 0 else 0 for x in rgb ])
            pixels[p] = rgb_r

            # Apply the same color to each LED in the block of 3
            for i in range(3):
                if p + i < n_leds:  # Ensure we don't go out of bounds
                    pixels[p + i] = rgb_r

        # write values
        pixels.show()
        time.sleep(delay)

def reverse_wave_effect(pixels, n_leds, duration=1.5, wave_color=(255, 96, 12)):
    """
    Creates a wave effect that lights up LEDs in reverse (from the last LED to the first one),
    keeping them on after they've been illuminated.

    :param pixels: The LED strip object.
    :param n_leds: Total number of LEDs in the strip.
    :param duration: Total duration of the wave effect in seconds.
    :param wave_color: The color of the wave in RGB format (default is a red/orange).
    """
    # Calculate delay per LED to cover the entire strip in the specified duration
    delay = duration / n_leds

    # Iterate through each LED in reverse order, lighting it up one by one
    for led in range(n_leds - 1, -3, -1):  # Start from last LED and go to the first
        # Set the current LED to the wave color
        pixels[led] = wave_color
        pixels[led-1] = wave_color
        pixels[led-2] = wave_color

        # Show the updated colors on the LED strip
        pixels.show()

        # Wait before lighting up the next LED
        time.sleep(delay)

        if led < 200:
            break

    # No need to reset LEDs, as they should stay on after the wave effect

#reverse_wave_effect(pixels, n_leds, duration=0.5)
fire_animation()
