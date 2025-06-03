import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd
import time
import paramiko
import os
import json
import numpy as np  # Import numpy

SENSOR_NAMES = ["MQ135_VOC", "MQ7_CarbonMonoxide"]
CONFIG_FILE = "configuration.json"

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

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_host, username=ssh_user, password=ssh_password)
    sftp = ssh.open_sftp()
    LOG_FILE = sftp.open(ssh_path, 'r')  # LOG_FILE is now a file-like object

    # Now you can use LOG_FILE with pandas:
    df = pd.read_csv(LOG_FILE, header=None, names=['timestamp', 'channel', 'sensor_name', 'adcOut', 'ppm'])
    LOG_FILE.close()
    sftp.close()
    ssh.close()

elif connection_type == "sshfs":
    sshfs_mount = config.get("sshfs_mount")
    local_path = config.get("local_path") or "sensor_log.csv"
    LOG_FILE = os.path.join(sshfs_mount, os.path.basename(local_path))

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
            ssh_host = config.get("ssh_host")
            ssh_user = config.get("ssh_user")
            ssh_path = config.get("ssh_path")
            ssh_password = config.get("ssh_password", None)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ssh_host, username=ssh_user, password=ssh_password)
            sftp = ssh.open_sftp()
            with sftp.open(ssh_path, 'r') as LOG_FILE:
                df = pd.read_csv(LOG_FILE, header=None, names=['timestamp', 'channel', 'sensor_name', 'adcOut', 'ppm'])
            sftp.close()
            ssh.close()
        else:
            if os.path.exists(LOG_FILE):
                df = pd.read_csv(LOG_FILE, header=None, names=['timestamp', 'channel', 'sensor_name', 'adcOut', 'ppm'])
            else:
                df = pd.DataFrame(columns=['timestamp', 'channel', 'sensor_name', 'adcOut', 'ppm'])

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
                    ax.plot(df_sensor['timestamp'], df_sensor['adcOut'], label='adcOut', color='cyan', marker='o')
                    ax.plot(df_sensor['timestamp'], df_sensor['ppm'], label='ppm', color='magenta', marker='x')
                ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
                ax.set_xlim([window_start, now])
                ax.set_ylim(0, 1000)

        plt.pause(0.5)

    plt.close(fig)

if __name__ == "__main__":
    plot_live()
# This script will continuously read from the sensor_log.csv file and plot the adcOut and ppm values in real-time.
# Make sure to run the sensor logging script in parallel to generate the log file.