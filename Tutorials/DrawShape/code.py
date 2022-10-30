# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test script for 2.9" 296x128 grayscale display.

Supported products:
  * Adafruit 2.9" Grayscale
    * https://www.adafruit.com/product/4777
  """

import time
import busio
import board
import displayio
import adafruit_il0373
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.polygon import Polygon

displayio.release_displays()

# This pinout works on a Feather M4 and may need to be altered for other boards.
spi = busio.SPI(board.SCK, board.MOSI)  # Uses SCK and MOSI
epd_cs = board.D9
epd_dc = board.D10

BLACK = 0x000000
WHITE = 0xFFFFFF
LIGHTGREY = 0x999999
DARKGREY = 0x666666

FOREGROUND_COLOR = BLACK
BACKGROUND_COLOR = WHITE

WIDTH = 296
HEIGHT = 128

display_bus = displayio.FourWire(
    spi, command=epd_dc, chip_select=epd_cs, baudrate=1000000
)
time.sleep(1)

display = adafruit_il0373.IL0373(
    display_bus,
    width=WIDTH,
    height=HEIGHT,
    rotation=270,
    black_bits_inverted=False,
    color_bits_inverted=False,
    grayscale=True,
    refresh_time=1,
)

g = displayio.Group()

# Set a white background
background_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
# Map colors in a palette
palette = displayio.Palette(1)
palette[0] = BACKGROUND_COLOR

# Create a  Tilegrid with the background and put in the displayio group
t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
g.append(t)

# Draw star
polygon = Polygon(
    [
        (255, 40),
        (262, 62),
        (285, 62),
        (265, 76),
        (275, 100),
        (255, 84),
        (235, 100),
        (245, 76),
        (225, 62),
        (248, 62),
    ],
    outline=BLACK,
)
g.append(polygon)

triangle = Triangle(170, 20, 140, 90, 210, 100, fill=LIGHTGREY, outline=BLACK)
g.append(triangle)

rect = Rect(80, 20, 41, 41, fill=LIGHTGREY, outline=DARKGREY, stroke=6)
g.append(rect)

circle = Circle(100, 100, 20, fill=WHITE, outline=BLACK)
g.append(circle)

rect2 = Rect(70, 85, 60, 30, outline=0x0, stroke=3)
g.append(rect2)

roundrect = RoundRect(10, 10, 61, 51, 10, fill=DARKGREY, outline=BLACK, stroke=6)
g.append(roundrect)

# Place the display group on the screen
display.show(g)

# Refresh the display to have everything show on the display
# NOTE: Do not refresh eInk displays more often than 180 seconds!
display.refresh()
