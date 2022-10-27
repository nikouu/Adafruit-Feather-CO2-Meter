# Adafruit-Feather-CO2-meter
Create a carbon dioxide meter with an Adafruit RP2040, a 2.9" eInk display, a SCD-40 CO2 sensor, and CircuitPython.

## Components

| Item                                                                                        | Notes                                                             |
| ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [Feather RP2040](https://www.adafruit.com/product/4884)                                     |                                                                   |
| [Adafruit 2.9" Grayscale eInk](https://www.adafruit.com/product/4777)                       | [Docs](https://docs.circuitpython.org/projects/il0373/en/latest/) |
| [Lithium Ion Polymer Battery 400mAh](https://www.adafruit.com/product/3898)                 |                                                                   |
| [SCD-40 - True CO2, Temperature and Humidity Sensor](https://www.adafruit.com/product/5187) |                                                                   |
| [STEMMA QT / Qwiic JST SH 4-pin Cable](https://www.adafruit.com/product/4210)               |                                                                   |
| [Brass M2.5 Standoffs 16mm tall](https://www.adafruit.com/product/2337)                     |                                                                   |

## Development

### Blink LED

### Running display

### Getting CO2 values

### First proof of concept

### Stable release

### Improvements

#### Power saving with a deep sleep


The battery lasts about 12 hours with the first stable release and I think it can do far better. But first, let's understand the power usage patterns. 

| Scenario | Description                    | Reading | Notes                                                                 |
| -------- | ------------------------------ | ------- | --------------------------------------------------------------------- |
| 1        | Blinking LED, nothing attached |         |                                                                       |
| 2        | Blinking LED, display          |         | The same as scenario 1, which makes sense, and which is why I ♥ eInk |
| 3        | Blinking LED, display, SCD-40  |         | Pretty much the same as scenario 1, maybe a smidge more at times      |
| 4        | Stable release code            |         | A smidge more again, but with some big spikes (see further down)      |

*Note: These do not describe the slight range of power consumption but they are readings of the most usual values*

Now that we have baseline measurements, it's time to optimise! 

Let's deal with the easy stuff: Busy waits. I love optimising things (self plug: [Shrinking a Self-Contained .NET 6 Wordle-Clone Executable](https://www.nikouusitalo.com/blog/shrinking-a-self-contained-net-6-wordle-clone-executable/)) and there's a whole heap of ways for programs to sleep across different languages. I suspect that in CircuitPython that the `time.sleep()` call might be a bit busy in the background during the wait period. Doing some digging, it turns out we can use alarms instead of sleeps. I picked up on this fantastic tutorial called [Deep Sleep with CircuitPython](https://learn.adafruit.com/deep-sleep-with-circuitpython/alarms-and-sleep) which explained the different types of sleep in CircuitPython. 

I ran some tests (which are in the Tutorials/DeepSleep folder) for deep sleeps. The test case was a blink based on the tutorial and here are the results:

| Scenario | Description                                | Reading     | Notes                                                                                                                  |
| -------- | ------------------------------------------ | ----------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1        | `time.sleep()`                             | 0.21W-0.23W |                                                                                                                        |
| 2        | `alarm.light_sleep_until_alarms()`         | 0.17W-0.25W | But more often around 0.17W-0.23W                                                                                      |
| 3        | `alarm.exit_and_deep_sleep_until_alarms()` | 0.11W-0.23W | Both: <ol><li>I did see it hit 0W a couple of times</li><li>The RGB NeoPixel also fires due to it booting up</li></ol> |

*Note: Test when connected to a power supply, and not PC as the board will not actively sleep when connected to a host computer.*


Every 3-5 seconds, the SCD-40 sensor does a reading regardless of whether the values will be read or not. This produces a little spike is power usage as seen below:

| Scenario      | Reading                         |
| ------------- | ------------------------------- |
| Regular usage | ![](images%5Cregular-usage.jpg) |
| Wattage spike | ![](images%5Cwattage-spike.jpg) |

*The reader in the images is the [Multifunctional USB Digital Tester - USB A and C](https://www.adafruit.com/product/4232).*










#### Can we turn off the sensor when not in use?

The sensor uses the on-board STEMMA QT connector. 