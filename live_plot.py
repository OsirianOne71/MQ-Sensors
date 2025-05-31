import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd
import time
import os

SENSOR_NAMES = ["MQ135_VOC", "MQ7_CarbonMonoxide"]
LOG_FILE = "sensor_log.csv"
WINDOW_MINUTES = 2

plt.style.use('dark_background')

def plot_live():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    fig.patch.set_facecolor('black')

    while True:
        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE, header=None, names=['timestamp', 'channel', 'sensor_name', 'adcOut', 'ppm'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            now = datetime.now()
            window_start = now - timedelta(minutes=WINDOW_MINUTES)

            for i, sensor_name in enumerate(SENSOR_NAMES):
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
                    ax.yaxis.set_tick_params(labelleft=True, colors='white')  # Force y-tick labels on right plot
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))

                df_sensor = df[(df['sensor_name'] == sensor_name) & (df['timestamp'] >= window_start)]
                ax.plot(df_sensor['timestamp'], df_sensor['adcOut'], label='adcOut', color='cyan')
                ax.plot(df_sensor['timestamp'], df_sensor['ppm'], label='ppm', color='magenta')
                ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
                ax.set_xlim([window_start, now])
                ax.set_ylim(0, 1000)  # Set y-axis (vertical) limits to 0-1000

        plt.pause(5)
        # time.sleep(5)  # Optional: sleep to reduce CPU usage, and data collection frequency is also 5 seconds

if __name__ == "__main__":
    plot_live()

# This script will continuously read from the sensor_log.csv file and plot the adcOut and ppm values in real-time.
# Make sure to run the sensor logging script in parallel to generate the log file.