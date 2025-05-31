#! /usr/bin/env python
# python program to communicate with an MCP3008
# Import our SpiDev wrapper and our sleep function

import spidev
from time import sleep, strftime
from datetime import datetime
import time
# Import the time module for log entries and sleep functionality

# Establish SPI device on Bus 0,Device 0
spi = spidev.SpiDev()
spi.open(0,0)

# Set SPI speed and mode | See spi_freq.txt for more info
spi.max_speed_hz = 500000 #500 kHz
spi.mode = 0b00  # Mode 0: CPOL=0, CPHA=0

# Function to log sensor data to a file
def log_to_file(channel, sensor_name, adcOut, ppm):
    with open("sensor_log.csv", "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        f.write(f"{timestamp},{channel},{sensor_name},{adcOut},{ppm}\n")


# Function to read ADC value from a specified channel and log it to a file
def getAdc(channel, sensor_name):
    #check valid channel
    if ((channel > 7) or (channel < 0)):
        return -1
    
    # Perform SPI transaction and store returned bits in 'r'
    r = spi.xfer([1, (8 + channel) << 4, 0])

    # Filter data bits from returned bits
    adcOut = ((r[1] & 3) << 8) + r[2]
    ppm = int(round(adcOut * 0.977517)) 
    # Convert ADC value to PPM 
    # (max 10-1000 PPM sensor resolution 1023 = 0.977517)
    # Sensor's characteristics, can be fine tuned by adjusting the potentiometer on the sensor board or by changing the conversion factor

    # Print the channel, sensor name, ADC output, and PPM value
    #uncomment the next line to enable printing to console
    #print(f"Channel: {channel} | Sensor: {sensor_name} | ADC Output: {adcOut:4d} | PPM: {ppm:4d}")
    
    # Log the data to a file
    log_to_file(channel, sensor_name, adcOut, ppm)

while True:
    start_time = time.time()
    getAdc(0, "MQ135_VOC")
    getAdc(1, "MQ7_CarbonMonoxide")
    #Measurement delay to save resources and avoid logging too frequently
    elapsed = time.time() - start_time
    sleep_time = max(0, 5 - elapsed)
    time.sleep(sleep_time)
    