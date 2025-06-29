#! /usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd
import time
import paramiko
import os
import json
import numpy as np  # Import numpy
import requests
import pytz

SENSOR_NAMES = [
    "MQ7_CO",
    "MQ137_VOC",
    "BME280_Temperature_F",
    "BME280_Pressure_hPA",
    "BME280_Humidity"
]
CONFIG_FILE = "configuration.json"

# Stream over SSH or SSHFS is for running the dasboard or android app on a remote machine
# Local is for running the dashboard on the same machine as the sensor logging script

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
else:
    config = {}

connection_type = config.get("connection_type", "Local").lower()

if connection_type == "local":
    LOG_FILE = config.get("local_path") or "sensor_log.csv"

elif connection_type == "stream over ssh":
    ssh_host = config.get("ssh_host")
    ssh_user = config.get("ssh_user")
    ssh_path = config.get("ssh_path")
    ssh_password = config.get("ssh_password", None)  # If you want to use password auth

    if not all([ssh_host, ssh_user, ssh_path]):
        raise ValueError("Missing SSH configuration: ssh_host, ssh_user, and ssh_path must all be set in configuration.json")

    if ssh_path is None:
        raise ValueError("ssh_path must not be None for SSH connection.")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(str(ssh_host), username=str(ssh_user), password=ssh_password)
    sftp = ssh.open_sftp()
    import io
    LOG_FILE = sftp.open(str(ssh_path), 'r')  # LOG_FILE is now a file-like object

    # Read the file content and use StringIO for pandas
    file_content = LOG_FILE.read().decode('utf-8')
    df = pd.read_csv(
        io.StringIO(file_content),
        header=None,
        names=['timestamp', 'channel', 'sensor_name', 'sensor_out', 'adj_value', 'adj_value_name']
    )
    LOG_FILE.close()
    sftp.close()
    ssh.close()

elif connection_type == "sshfs":
    sshfs_mount = config.get("sshfs_mount")
    local_path = config.get("local_path") or "sensor_log.csv"
    if not sshfs_mount:
        raise ValueError("sshfs_mount must be set in configuration.json for sshfs connection.")
    LOG_FILE = os.path.join(str(sshfs_mount), str(os.path.basename(local_path)))

else:
    LOG_FILE = "sensor_log.csv"

WINDOW_MINUTES = 2
screen_duration = int(config.get("screen_duration", 5))
zip_code = config.get("zip_code", "37757")
time_zone = config.get("time_zone", "America/New_York")

plt.style.use('dark_background')

def plot_live():
    fig, axes = plt.subplots(1, 1, figsize=(14, 6))
    plt.show(block=False)
    fig.patch.set_facecolor('black')
    screen_idx = 0
    last_switch = time.time()

    while True:
        if not plt.fignum_exists(fig.number):
            break

        now = time.time()
        if now - last_switch > screen_duration:
            screen_idx = (screen_idx + 1) % 3
            last_switch = now

        axes.clear()
        if screen_idx == 0:
            plot_indoor(axes)
        elif screen_idx == 1:
            plot_current_weather(axes, zip_code, time_zone)
        elif screen_idx == 2:
            plot_forecast(axes, zip_code, time_zone)

        plt.pause(0.5)
    plt.close(fig)

def plot_indoor(ax):
    # Your existing code to plot local sensor data
    ax.set_title("Indoor Air Quality", color='white')
    # ...plotting logic...

def plot_current_weather(ax, zip_code, time_zone):
    # Query weather API for current and next 4 hours
    ax.set_title(f"Current Weather ({zip_code})", color='white')
    # ...plotting logic...

def plot_forecast(ax, zip_code, time_zone):
    # Query weather API for next 4 days
    ax.set_title(f"4-Day Forecast ({zip_code})", color='white')
    # ...plotting logic...

if __name__ == "__main__":
    plot_live()
# This script will continuously read from the sensor_log.csv and or sensor_data.db file and plot outputs in real-time
# Historical data can be viewed by running the script without the live plotting functionality
# Make sure to run the sensor logging script and install the service in parallel to generate the log file