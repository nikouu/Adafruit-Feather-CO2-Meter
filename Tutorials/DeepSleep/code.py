# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
# https://learn.adafruit.com/adafruit-feather-rp2040-pico/blink
"""CircuitPython Blink Example - the CircuitPython 'Hello, World!'"""
import time
import alarm
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(1)
    led.value = False

    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 3)
    alarm.light_sleep_until_alarms(time_alarm)