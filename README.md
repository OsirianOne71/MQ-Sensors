# MQ135-AirQuality
Python code for RPI and MCP3008 to connect up to 8 sensor(s), data log, display, alert, configuration data.

**Introduction**
The MCP3008 is an 8-channel, 10-bit analog-to-digital converter (ADC) manufactured by MCP. It is designed to convert analog signals into digital data, enabling microcontrollers to process and interpret analog inputs. The MCP3008 communicates using the SPI (Serial Peripheral Interface) protocol, which ensures fast and reliable data transfer. This component is widely used in embedded systems for interfacing with sensors, potentiometers, and other analog devices.
    https://docs.cirkitdesigner.com/component/e3afbb86-da52-4bd2-b1c8-3669dd5bcd79/mcp3008
    https://www.allelcoelec.com/blog/A-Complete-Overview-of-the-MCP3008-ADC.html

**How to Use the MCP3008 in a Circuit**
   - Power Supply: Connect the VDD pin to a 3.3V or 5V power source, and connect the AGND and DGND pins to ground. (Set to same level as the sensor uses)
   - Reference Voltage: Connect the VREF pin to a stable reference voltage (e.g., 3.3V or 5V). This determines the ADC's input range. 5V gives a resolution of 0-1023 and increases accuracy.

**SPI Connections:**
Connect the CS/SHDN pin to a GPIO pin on the microcontroller for chip select
Connect the DIN pin to the SPI MOSI pin on the microcontroller
Connect the DOUT pin to the SPI MISO pin on the microcontroller
Connect the CLK pin to the SPI SCK pin on the microcontroller
Analog Inputs: Connect up to 8 analog signals to the CH0–CH7 pins. Ensure the input voltage does not exceed VREF.
SPI Configuration: Configure the microcontroller's SPI interface to communicate with the MCP3008.    Code config = SPI mode 0 (CPOL = 0, CPHA = 0)

**Wiring:**
Between the [MCP3008](https://microcontrollerslab.com/wp-content/uploads/2020/03/MCP3008-Simple-Connection-Diagram.jpg) and [Raspberry Pi](https://pinout.xyz/):
Chip orientation is marked by a small semi-circular indentation on top of the chip.

Wire up as shown in the [wire scheme](https://www.instructables.com/Wiring-up-a-MCP3008-ADC-to-a-Raspberry-Pi-model-B-/) 

    MCP3008 pin 16 VDD  -> VDD        RPi pin 02  5V  (red)    Can not exceed the VREF
    MCP3008 pin 15 VREF -> VREF       RPi pin 04  5V  (red)    Must Match sensor voltage used
    MCP3008 pin 14 AGND -> GND        RPi pin 05  GND (black)
    MCP3008 pin 13 CLK  -> SPi SCLK   RPi pin 23  (orange) (SPI Clock)
    MCP3008 pin 12 DOUT -> SPI MISO   RPi pin 21  (yellow)
    MCP3008 pin 11 DIN  -> SPI MOSI   RPi pin 19  (blue)
    MCP3008 pin 10 CS   -> GPIO 23    RPi pin 24  (violet) --Conf in code as Chip Select 0(off)/1(on)
    MCP3008 pin 09 DGND -> GND        RPi pin 25  (black)

   **DUE TO CURRENT DRAW OF 1 OR MORE SENSORS; THE VDD AND GND OF THE SENSOR WILL LIKELY NEED SEPERATE SUPPLIED POWER - THIS WILL ENSURE LOW NOISE AND CLEARER READINGS ALONG WITH OPTIONAL DECOUPLING CAPACITOR ON MCP3008 PIN 16**

**Important Considerations and Best Practices**
   + **Input Voltage Range:** Ensure the analog input voltage does not exceed VREF to avoid damage or incorrect (noisy) readings
   + **Decoupling Capacitors:** Place a 0.1 µF ceramic capacitor close to the VDD pin to reduce noise
   + **SPI Speed:** Use an appropriate SPI clock speed (e.g., 1 MHz) to ensure reliable communication
   + **Unused Channels:** If not all channels are used, connect unused channels to ground to prevent floating inputs, this can also create 'noise"

**# Troubleshooting and FAQs**
**Common Issues and Solutions**

**1. No Output or Incorrect Readings:**
   - Verify all connections, especially SPI pins and power supply
   - Ensure the CS/SHDN pin is correctly toggled during communication
   - Check that the SPI mode is set to mode 0 (CPOL = 0, CPHA = 0)

**2. Floating or Noisy Readings:**
   - Ensure unused analog input channels are connected to ground
   - Use proper shielding and grounding techniques to minimize noise

**3. Low Accuracy or Resolution:**
   - Verify that the reference voltage (VREF) is stable and noise-free
   - Ensure the input signal is within the specified range (2.7V to VREF : max 5V)
   - Can optionally add a decoupling capacitor to the VDD Pin 16



**SAMPLE PROJECT**
   To Test this project a Air Quality sensor that has an A0 (Analog output) that is connected to a channel 0 (Pin1) on the ADC Converter (MCP3008 above) that will change the value into a Digital number and calculate Percentage of that save value.

[MQ135 Air Quality Sensor](https://www.elprocus.com/mq135-air-quality-sensor/) | Detection of Volatile Organic Compound (VOC) - potential dangerous in certain PPMs

   An MQ135 air quality sensor is one type of MQ gas sensor used to detect, measure, and monitor a wide range of gases present in air like ammonia, alcohol, benzene, smoke, carbon dioxide, etc. It operates at a 5V supply with 150mA consumption. Preheating of 20 seconds is required before the operation, to obtain the accurate output.

![MQ135 Pin Configuration](![https://www.elprocus.com/wp-content/uploads/MQ135-Air-Quality-Sensor-Pin-Configuration-300x152.jpg])
   - VCC pin -> RPi pin 04 5V       (red)
   - GND pin -> RPi pin 06 GND      (black)
   - Do  pin -> unconnected
   - Ao  pin -> MCP3008 CH0-pin 01  (green)

Now that we wired up lets convert analog inputs to digital outputs!
   1. Boot and Log into your Raspberry PI
   2. Complete the wiring
   3. Open Terminal > sudo raspi-config > 2-Interfaces > Set SPI to ON
   4. Clone the Repository > cd MQ135-airquality
   5. Create .venv environment and activate
   6. pip install spidev
      - to test that the RPi is configured for spi
      - Open Terminal > 
   7. python3 MQ135.py
