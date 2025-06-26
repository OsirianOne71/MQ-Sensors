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

SENSOR_NAMES = ["MQ135_VOC", "MQ007_CO"]
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

plt.style.use('dark_background')

def plot_live():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    axes = np.array(axes).flatten()
    plt.show(block=False)
    fig.patch.set_facecolor('black')

    while True:
        if not plt.fignum_exists(fig.number):
            break

        if connection_type == "stream over ssh":
            ssh_host = str(config.get("ssh_host") or "")
            ssh_user = str(config.get("ssh_user") or "")
            ssh_path = str(config.get("ssh_path") or "")
            ssh_password = config.get("ssh_password", None)
            if not all([ssh_host, ssh_user, ssh_path]):
                raise ValueError("Missing SSH configuration: ssh_host, ssh_user, and ssh_path must all be set in configuration.json")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ssh_host, username=ssh_user, password=ssh_password)
            sftp = ssh.open_sftp()
            import io
            with sftp.open(ssh_path, 'r') as LOG_FILE:
                file_content = LOG_FILE.read().decode('utf-8')
                df = pd.read_csv(
                    io.StringIO(file_content),
                    header=0  # Use header row from file
                )
            sftp.close()
            ssh.close()
        else:
            if isinstance(LOG_FILE, str) and os.path.exists(LOG_FILE):
                df = pd.read_csv(
                    LOG_FILE,
                    header=0  # Use header row from file
                )
            else:
                df = pd.DataFrame(
                    columns=['timestamp', 'channel', 'sensor_name', 'sensor_out', 'adj_value', 'adj_value_name']
                )

        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            now = datetime.now()
            window_start = now - timedelta(minutes=WINDOW_MINUTES)

            for i, sensor_name in enumerate(SENSOR_NAMES):
                df_sensor = df[(df['sensor_name'] == sensor_name) & (df['timestamp'] >= window_start)]
                ax = axes[i]
                ax.clear()
                ax.set_facecolor('black')
                ax.set_title(sensor_name, color='white')
                ax.set_xlabel("Time (2 Minutes)", color='white')
                if i == 0:
                    ax.set_ylabel("PPM", color='white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                if i == 1:
                    ax.yaxis.set_tick_params(labelleft=True, colors='white')
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))

                # Only plot if there is data
                if not df_sensor.empty:
                    ax.plot(df_sensor['timestamp'], df_sensor['sensor_out'], label='sensor_out', color='cyan', marker='o')
                    ax.plot(df_sensor['timestamp'], df_sensor['adj_value'], label='adj_value', color='magenta', marker='x')
                ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
                ax.set_xlim([window_start, now])
                ax.set_ylim(0, 1000)

        plt.pause(0.5)

    plt.close(fig)

if __name__ == "__main__":
    plot_live()
# This script will continuously read from the sensor_log.csv and or sensor_data.db file and plot outputs in real-time
# Historical data can be viewed by running the script without the live plotting functionality
# Make sure to run the sensor logging script and install the service in parallel to generate the log file