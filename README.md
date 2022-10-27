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

## Power saving attempts

The battery lasts about 12 hours with the first iteration of code and I think it can do far better.

### CO2 sensor

Every 3-5 seconds, the SCD-40 sensor does a reading regardless of whether the values will be read or not. This produces a little spike is power usage as seen below:

| Explanation   | Image                           |
| ------------- | ------------------------------- |
| Regular usage | ![](images%5Cregular-usage.jpg) |
| Wattage spike | ![](images%5Cwattage-spike.jpg) |

*The reader in the images is the [Multifunctional USB Digital Tester - USB A and C](https://www.adafruit.com/product/4232).*

#### Can we turn off the sensor when not in use?

The sensor uses the on-board STEMMA QT connector. 