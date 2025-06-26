#! /usr/bin/env python3
# This script is started as a cron -e job to run at midnight (00:00:00) each day
# Rotate the sensor_log.csv file, push its data to SQLite, and clean up old CSVs
# command to set up the cron job:
# crontab -e
# 59 23 * * * /usr/bin/python3 /home/choll/rotate_csv.py

import os
import shutil
import sqlite3
from datetime import datetime, timedelta
import csv

BASE_DIR = "/home/choll"
CSV_PATH = os.path.join(BASE_DIR, "sensor_log.csv")
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
DB_PATH = os.path.join(BASE_DIR, "sensor_data.db")

# Ensure archive folder exists
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Step 1: Push current CSV data into SQLite
def push_csv_to_sqlite(csv_path, db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        channel TEXT,
        sensor_name TEXT,
        sensor_out REAL,
        adj_value REAL,
        adj_value_name TEXT
    )''')

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if len(row) == 6:
                c.execute('INSERT INTO sensor_data (timestamp, channel, sensor_name, sensor_out, adj_value, adj_value_name) VALUES (?, ?, ?, ?, ?, ?)', row)

    conn.commit()
    conn.close()

# Step 2: Rename CSV
def rotate_csv():
    if not os.path.exists(CSV_PATH):
        print("No sensor_log.csv to rotate.")
        return
    date_str = datetime.now().strftime("%Y-%m-%d")
    archive_path = os.path.join(ARCHIVE_DIR, f"sensor_log_{date_str}.csv")
    shutil.move(CSV_PATH, archive_path)
    with open(CSV_PATH, "w") as f:
        f.write("timestamp,channel,sensor_name,sensor_out,adj_value,adj_value_name\n")

# Step 3: Delete CSVs older than 7 days
def clean_old_csvs():
    cutoff = datetime.now() - timedelta(days=7)
    for filename in os.listdir(ARCHIVE_DIR):
        if filename.startswith("sensor_log_") and filename.endswith(".csv"):
            date_str = filename[12:-4]
            try:
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                if file_date < cutoff:
                    os.remove(os.path.join(ARCHIVE_DIR, filename))
            except ValueError:
                continue

# Main routine
if __name__ == "__main__":
    push_csv_to_sqlite(CSV_PATH, DB_PATH)
    rotate_csv()
    clean_old_csvs()
