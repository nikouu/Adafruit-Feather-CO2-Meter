import time
import alarm
import busio
import board
import displayio
import terminalio
import adafruit_il0373
import adafruit_scd4x
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_bitmap_font import bitmap_font

WIDTH = 296
HEIGHT = 128

BLACK = 0x000000
DARKGREY = 0x666666
LIGHTGREY = 0x999999
WHITE = 0xFFFFFF

FOREGROUND_COLOR = BLACK
BACKGROUND_COLOR = WHITE

VERDANA_BOLD = "/fonts/Verdana-Bold-18.bdf"

def trigger_single_sensor_measurement(scd4x):
    scd4x.start_periodic_measurement()
    while not scd4x.data_ready:
        time.sleep(1)

    co2 = scd4x.CO2
    temperature = scd4x.temperature
    relative_humidity = scd4x.relative_humidity

    scd4x.stop_periodic_measurement()

    return co2, temperature, relative_humidity

def get_co2_wording(value):
    if value == 69:
        return "NICE"
    elif value == 420:
        return "BLAZE"
    elif value == 666:
        return "EVIL"
    elif value == 1337:
        return "LEET"
    elif value < 800:
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

verdana_bold_font = bitmap_font.load_font(VERDANA_BOLD)

spi = busio.SPI(board.SCK, board.MOSI)  # Uses SCK and MOSI
epd_cs = board.D9
epd_dc = board.D10

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

tile_grid = displayio.Group()
palette = displayio.Palette(1)
palette[0] = BACKGROUND_COLOR

t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
tile_grid.append(t)

try:
    i2c = board.I2C()
    scd4x = adafruit_scd4x.SCD4X(i2c)
    
    co2, temperature, relative_humidity = trigger_single_sensor_measurement(scd4x)

    co2_background_rect = Rect(2, 2, 189, 124, fill=DARKGREY, outline=0x0, stroke=0)
    tile_grid.append(co2_background_rect)

    temperature_background_rect = Rect(193, 2, 101, 61, fill=DARKGREY, outline=0x0, stroke=0)
    tile_grid.append(temperature_background_rect)

    humidity_background_rect = Rect(193, 65, 101, 61, fill=DARKGREY, outline=0x0, stroke=0)
    tile_grid.append(humidity_background_rect)

    co2_value_text_group = create_text_group(27, 90, terminalio.FONT, "%d ppm" % co2, 3, WHITE)
    tile_grid.append(co2_value_text_group)

    temperature_text_group = create_text_group(199, 30, terminalio.FONT, "%0.1fC" % temperature, 3, WHITE)
    tile_grid.append(temperature_text_group)

    humidity_text_group = create_text_group(199, 90, terminalio.FONT, "%0.1f%%" % relative_humidity, 3, WHITE)
    tile_grid.append(humidity_text_group)

    co2_text_group = create_text_group(25, 35, verdana_bold_font, get_co2_wording(co2), 2, WHITE)
    tile_grid.append(co2_text_group)

except RuntimeError as err:
    error_text_group = create_text_group(10, 10, terminalio.FONT, str(err), 1, BLACK)
    tile_grid.append(error_text_group)


display.show(tile_grid)
display.refresh()	

time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 300)
alarm.exit_and_deep_sleep_until_alarms(time_alarm)