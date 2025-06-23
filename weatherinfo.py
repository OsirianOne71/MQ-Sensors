#! /usr/bin/env python3
# python program to communicate with an MCP3008 and BME280
# Import our SpiDev wrapper and our sleep function

import spidev
from time import sleep, strftime
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
import os
import board
import busio
import math
import adafruit_bme280.advanced

# Establish SPI device on Bus 0,Device 0
spi = spidev.SpiDev() # Create an instance of SpiDev on the Raspberry Pi
spi.open(0,0) # Open SPI bus 0, device 0 (MCP3008_0-0)

# Set SPI speed and mode | See spi_freq.txt for more info
spi.max_speed_hz = 500000 #500 kHz
spi.mode = 0b00  # Mode 0: CPOL=0, CPHA=0 | Clock polarity and phase

# === BME280 Setup ===
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.advanced.Adafruit_BME280_I2C(i2c)
# bme280.sea_level_pressure = 1013.25  # Default, adjust for your local pressure
bme280.sea_level_pressure = 1010  # Jacksboro, TN 37757 calibration

CSV_FILE = "sensor_log.csv"
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, "w") as f:
        f.write("timestamp,channel,sensor_name,sensor_out,adj_value,adj_value_name\n")

# Function to log sensor data to a file with exception handling
def log_to_file(channel, sensor_name, sensor_out, adj_value, adj_value_name):
    try:
        with open(CSV_FILE, "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp},{channel},{sensor_name},{sensor_out},{adj_value},{adj_value_name}\n")
    except OSError as e:
        error_msg = f"[ERROR] Failed to write to log file: {e}"
        print(error_msg)
        send_error_email(error_msg)

# Function to send error email notifications
def send_error_email(error_message):
    # Configure these settings for your email provider
    smtp_server = "smtp.provider.com" # Replace with your SMTP server
                                    # Example: smtp.gmail.com for Gmail
    smtp_port = 587 # Use 465 for SSL
    smtp_user = "youremail.com"  # Replace with your email address
    smtp_password = "password"   # Use an app password if 2FA is enabled
    to_email = "youremail.com"   # Replace with the recipient's email address

    msg = MIMEText(f"Sensor logging error:\n\n{error_message}")
    msg["Subject"] = "Raspberry Pi Sensor Logging Error"
    msg["From"] = smtp_user
    msg["To"] = to_email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
    except Exception as e:
        print(f"[ERROR] Failed to send error email: {e}")

# Function to read ADC value from a specified channel and log it to a file
def getAdc(channel, sensor_name, channel_name):
    if ((channel > 7) or (channel < 0)):
        return -1

    r = spi.xfer([1, (8 + channel) << 4, 0])
    adcOut = ((r[1] & 3) << 8) + r[2]

    # Get latest BME280 readings for correction
    temp_c = bme280.temperature
    humidity = bme280.humidity

    if sensor_name == "MQ135_VOC":
        # Use MQ135 correction formula for MQ135_VOC (adjust if you have MQ135-specific formula)
        adj_value = mq135_get_corrected_ppm(adcOut, temp_c, humidity, MQ135_R0, MQ135_RL)
        adj_value_name = "ppm"
    else:
        # Default: just scale ADC value
        adj_value = round(adcOut * 0.977517, 2)
        adj_value_name = "ppm"

    print(f"{channel_name} | Sensor: {sensor_name} | sensor_out: {adcOut:4d} | adj_value: {adj_value:7.2f} {adj_value_name}")
    log_to_file(channel_name, sensor_name, adcOut, adj_value, adj_value_name)

def log_bme280():
    # Temperature in Celsius, convert to Fahrenheit
    temp_c = bme280.temperature
    temp_f = round(temp_c * 9 / 5 + 32, 2)
    humidity = round(bme280.humidity, 2)
    pressure = round(bme280.pressure, 2)
    channel = "BME280_i2c"
    # Log temperature
    print(f"{channel} | Sensor: BME280_Temperature_F | sensor_out: {temp_c:.2f}C | adj_value: {temp_f:.2f} F")
    log_to_file(channel, "BME280_Temperature_F", temp_c, temp_f, "F")
    # Log humidity
    print(f"{channel} | Sensor: BME280_Humidity | sensor_out: {humidity:.2f} | adj_value: {humidity:.2f} %")
    log_to_file(channel, "BME280_Humidity", humidity, humidity, "%")
    # Log pressure
    print(f"{channel} | Sensor: BME280_Pressure_hPA | sensor_out: {pressure:.2f} | adj_value: {pressure:.2f} hPa")
    log_to_file(channel, "BME280_Pressure_hPA", pressure, pressure, "hPa")

def check_unknown_channels():
    unknown_channels = []
    for ch in range(2, 8):
        r = spi.xfer([1, (8 + ch) << 4, 0])
        adcOut = ((r[1] & 3) << 8) + r[2]
        if adcOut != 0:
            unknown_channels.append(ch)
    if unknown_channels:
        msg = f"Warning: Data detected on unknown MCP3008 channels: {unknown_channels}"
        print(msg)
        send_error_email(msg)

# Calibration constants for MQ135 (replace with your calibration values)
MQ135_R0 = 10000  # Ohms
MQ135_RL = 10000  # Ohms

def mq135_get_corrected_ppm(adcOut, temp_c, humidity, R0, RL):
    """
    Calculate corrected PPM for MQ135 sensor using environmental compensation.
    Args:
        adcOut: Raw ADC value (0-1023)
        temp_c: Temperature in Celsius
        humidity: Relative humidity in %
        R0: Sensor resistance in clean air (Ohms)
        RL: Load resistance (Ohms)
    Returns:
        corrected_ppm: Corrected gas concentration in PPM
    """
    # Convert ADC value to sensor voltage (assuming 3.3V ADC reference)
    Vadc = adcOut * 3.3 / 1023.0
    if Vadc == 0:
        return 0  # Avoid division by zero
    Rs = RL * (3.3 - Vadc) / Vadc

    # Environmental correction factor (from MQSensorsLib)
    a = 0.00035
    b = 0.02718
    c = 1.39538
    d = 0.0018
    corr_factor = a * temp_c * temp_c - b * temp_c + c - (humidity - 33.0) * d

    # Calculate ratio Rs/R0
    ratio = Rs / R0

    # MQ135 datasheet: PPM = 116.6020682 * (Rs/R0)^-2.769034857
    try:
        ppm = 116.6020682 * math.pow(ratio, -2.769034857)
    except (ValueError, ZeroDivisionError):
        ppm = 0

    # Apply environmental correction
    corrected_ppm = ppm * corr_factor
    return round(corrected_ppm, 2)
"""
Calibration Note:
-----------------
MQ-series sensors require calibration for accurate gas concentration readings.
- Collect temperature, humidity, and pressure (e.g., from BME280) before using MQ sensor data.
- Apply temperature and humidity corrections to the raw ADC value using a calibration formula,
  along with your sensors load resistance and baseline (R₀).
- See the MQSensorsLib GitHub repository for reference calibration code:
  https://github.com/miguel5612/MQSensorsLib

Current script logs temperature, humidity, and pressure, but does NOT yet apply environmental correction
to the MQ sensor readings. Add this logic for improved accuracy.
"""

try:
    while True:
        start_time = time.time()
        # MCP3008_0-0 Channels and Sensor names
        getAdc(0, "MQ135_VOC", "MCP00_CH00")
        getAdc(1, "MQ7_CO", "MCP00_CH01")
        # Add more getAdc() calls for additional channels/sensors if needed

        # BME280 sensor readings
        log_bme280()

        # Check for unknown MCP3008 channels with activity
        check_unknown_channels()

        #Measurement delay to save resources and avoid logging too frequently
        elapsed = time.time() - start_time
        print(f"Loop time: {elapsed:.3f} seconds")  # Show how long the loop took
        sleep_time = max(0, 5 - elapsed)
        time.sleep(sleep_time)
except KeyboardInterrupt:
    print("Terminated by user")
finally:
    spi.close()
