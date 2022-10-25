import time
import busio
import board
import displayio
import terminalio
import adafruit_il0373
import adafruit_scd4x
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_bitmap_font import bitmap_font

def get_co2_wording(value):
    if value < 800:
        return "GOOD"
    elif value < 1200:
        return "FAIR"
    elif value < 1500:
        return "POOR"
    elif value < 2000:
        return "GRIM"
    else:
        return "DIRE"

def create_text_group(x, y, font, text, scale, colour):
    text_group = displayio.Group(scale=scale, x=x, y=y)
    text_area = label.Label(font, text=text, color=colour)
    text_group.append(text_area)
    return text_group

displayio.release_displays()

font_name = "/fonts/Verdana-Bold-18.bdf"
font = bitmap_font.load_font(font_name)

spi = busio.SPI(board.SCK, board.MOSI)  # Uses SCK and MOSI
epd_cs = board.D9
epd_dc = board.D10

i2c = board.I2C()
scd4x = adafruit_scd4x.SCD4X(i2c)
scd4x.start_periodic_measurement()

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

background_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)

while True:
    g = displayio.Group()
    # Map colors in a palette
    palette = displayio.Palette(1)
    palette[0] = BACKGROUND_COLOR

    t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
    g.append(t)

    cO2Level = 0
    temperature = 0.0
    humidity = 0.0

    while not scd4x.data_ready:
        time.sleep(1)

    cO2Level = scd4x.CO2
    temperature = scd4x.temperature
    humidity = scd4x.relative_humidity

    co2_background_rect = Rect(2, 2, 189, 124, fill=DARKGREY, outline=0x0, stroke=0)
    g.append(co2_background_rect)

    temperature_background_rect = Rect(193, 2, 101, 61, fill=DARKGREY, outline=0x0, stroke=0)
    g.append(temperature_background_rect)

    humidity_background_rect = Rect(193, 65, 101, 61, fill=DARKGREY, outline=0x0, stroke=0)
    g.append(humidity_background_rect) 

    co2_value_text_group = create_text_group(27, 90, terminalio.FONT, "%d ppm" % cO2Level, 3, WHITE)
    g.append(co2_value_text_group)    

    temperature_text_group = create_text_group(199, 30, terminalio.FONT, "%0.1fC" % temperature, 3, WHITE)
    g.append(temperature_text_group)    
    
    humidity_text_group = displayio.Group(scale=3, x=199, y=90)
    humidity_text = "%0.1f%%" % humidity
    humidity_text_area = label.Label(terminalio.FONT, text=humidity_text, color=WHITE)
    humidity_text_group.append(humidity_text_area)  # Add this text to the text group
    g.append(humidity_text_group)
    
    co2_text_group = displayio.Group(scale=2, x=25, y=35)
    #co2_text = "CO2: %d ppm" % cO2Level
    co2_text = "GOOD"
    co2_text_area = label.Label(font, text=get_co2_wording(cO2Level), color=WHITE)
    co2_text_group.append(co2_text_area)  # Add this text to the text group
    g.append(co2_text_group)

    display.show(g)
    display.refresh()	
    time.sleep(300)