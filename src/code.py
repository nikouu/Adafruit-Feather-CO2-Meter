import time
import busio
import board
import displayio
import terminalio
import adafruit_il0373
import adafruit_scd4x
from adafruit_display_text import label

displayio.release_displays()

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

    co2_text_group = displayio.Group(scale=1, x=10, y=0)
    co2_text = "CO2: %d ppm" % cO2Level
    co2_text_area = label.Label(terminalio.FONT, text=co2_text, color=FOREGROUND_COLOR)
    co2_text_group.append(co2_text_area)  # Add this text to the text group
    g.append(co2_text_group)

    temperature_text_group = displayio.Group(scale=1, x=40, y=50)
    temperature_text = "Temperature: %0.1f *C" % temperature
    temperature_text_area = label.Label(terminalio.FONT, text=temperature_text, color=FOREGROUND_COLOR)
    temperature_text_group.append(temperature_text_area)  # Add this text to the text group
    g.append(temperature_text_group)

    humidity_text_group = displayio.Group(scale=1, x=80, y=100)
    humidity_text = "Humidity: %0.1f %%" % humidity
    humidity_text_area = label.Label(terminalio.FONT, text=humidity_text, color=FOREGROUND_COLOR)
    humidity_text_group.append(humidity_text_area)  # Add this text to the text group
    g.append(humidity_text_group)

    display.show(g)
    display.refresh()	
    time.sleep(180)