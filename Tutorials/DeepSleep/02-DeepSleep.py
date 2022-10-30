# https://learn.adafruit.com/deep-sleep-with-circuitpython/alarms-and-sleep

import time
import alarm
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

led.value = True
time.sleep(1)
led.value = False

time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 3)
alarm.exit_and_deep_sleep_until_alarms(time_alarm)