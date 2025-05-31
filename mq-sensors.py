#! /usr/bin/env python
# python program to communicate with an MCP3008
# Import our SpiDev wrapper and our sleep function

import spidev
from time import sleep, strftime
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
# Import the time module for log entries and sleep functionality

# Establish SPI device on Bus 0,Device 0
spi = spidev.SpiDev()
spi.open(0,0)

# Set SPI speed and mode | See spi_freq.txt for more info
spi.max_speed_hz = 500000 #500 kHz
spi.mode = 0b00  # Mode 0: CPOL=0, CPHA=0

# Function to log sensor data to a file
def log_to_file(channel, sensor_name, adcOut, ppm):
    try:
        with open("sensor_log.csv", "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            f.write(f"{timestamp},{channel},{sensor_name},{adcOut},{ppm}\n")
    except OSError as e:
        error_msg = f"[ERROR] Failed to write to log file: {e}"
        print(error_msg)
        send_error_email(error_msg)


# Function to send error email notifications
def send_error_email(error_message):
    # Configure these settings for your email provider
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "cholli.pers@gmail.com"
    smtp_password = "Isis1971!#"
    to_email = "cholli.pers@gmail.com"

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
    # Sensor's characteristics, fine tuned by adjusting potentiometer on sensor board or by changing conversion factor

    # Print the channel, sensor name, ADC output, and PPM value
    #uncomment the next line to enable printing to console
    print(f"Channel: {channel} | Sensor: {sensor_name} | ADC Output: {adcOut:4d} | PPM: {ppm:4d}")
    
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
