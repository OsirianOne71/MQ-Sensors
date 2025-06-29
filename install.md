🧪 Deployment Steps

## Installation Steps

1. **Open terminal on your Raspberry Pi Zero 2W**

2. **Clone the repository:**

```sh
cd ~
git clone https://github.com/OsirianOne71/MQ-Sensors.git
cd MQ-Sensors
```

3. **(Optional) Create a Python virtual environment:**

```sh
python3 -m venv .venv
source .venv/bin/activate
```

4. **Install Python dependencies:**

```sh
sudo pip install spidev matplotlib pandas smbus2 adafruit-circuitpython-bme280 
```

5. **Enable SPI and I2C interfaces:**

```sh
sudo raspi-config
```

Navigate to *Interface Options* > *Enable SPI*, *Enable I2C*, and *Enable SSH*.

6. **Warm-up time:** Wait \~2 minutes for sensors to stabilize.

7. **(OPTIONAL) Manually Run logging script:**

```sh
python3 sensor_logger.py
```

8. **Configure plotting environment:**

```sh
python3 settings.py
```

9. **View real-time data (optional):**

```sh
python3 dashboard.py
```

---

## Setup as a systemd Service

1. **Make scripts executable:**

```sh
chmod +x ~/weather_sensor/weather_logging.py
chmod +x ~/weather_sensor/rotate_csv.py
chmod +x ~/weather_sensor/settings.py
chmod +x ~/weather_sensor/dashboard.py
```

2. **Copy Service Files into Systemd:**

```sh
sudo cp rotate_csv.service /etc/systemd/system/
sudo cp rotate_csv.timer /etc/systemd/system/
sudo cp sensor_logger.service /etc/systemd/system
```

3. **Enable and start service:**

```sh
sudo systemctl daemon-reload

sudo systemctl enable rotate_csv.timer
sudo systemctl start rotate_csv.timer
sudo systemctl enable sensor_logger.service
sudo systemctl start sensor_logger.service
```

---

## Remote Log Access via SSHFS

### On Raspberry Pi:

1. Enable SSH:

```sh
sudo raspi-config
```

2. Find IP address:

```sh
hostname -I
```

### On Remote Linux/macOS Machine:

1. Install SSHFS:

```sh
sudo apt install sshfs  # Linux
brew install sshfs      # macOS
```

2. Mount Pi log directory:

```sh
mkdir -p ~/pi_logs
sshfs pi@<PI_IP>:/var/logs/ /var/logs/
```

3. Access log at 
   - `/var/logs/sensor_logger.service`
   - `/var/logs/rotate_csv.service`

4. Unmount:

```sh
fusermount -u /var/log/air-quality  # Linux
umount /var/log/air-quality         # macOS
```

### On Windows:

Use [WinFsp + SSHFS-Win](https://github.com/billziss-gh/sshfs-win) or [Dokan SSHFS](https://github.com/dokan-dev/dokany).

## Remote Plotting

1. Clone or copy:
   `dashboard.py`, `settings.py`, `configuration.json`
2. Configure:
```sh
python3 settings.py
```

3. Run:

```sh
python3 dashboard.py
```

---

## Troubleshooting

**No Output or Incorrect Readings:**

- Check wiring and SPI pin setup
- Ensure SPI mode is set to 0 (CPOL=0, CPHA=0)
- Ensure the CS pin is toggled correctly in code

**Floating or Noisy Readings:**

- Ground all unused channels
- Use shielding and proper layout practices

**Low Accuracy:**

- Ensure stable VREF and signal within range
- Use optional decoupling capacitors



ADDITONAL NOTES:

# Copy files into systemd
sudo cp rotate_csv.service /etc/systemd/system/
sudo cp rotate_csv.timer /etc/systemd/system/
sudo cp sensor_logger.service /etc/systemd/system

# Reload systemd to recognize new files
sudo systemctl daemon-reload

# Enable and start the timer
sudo systemctl enable rotate_csv.timer
sudo systemctl start rotate_csv.timer

# Enable, start and verify the services
sudo systemctl enable rotate_csv.service
sudo systemctl start rotate_csv.service

sudo systemctl enable sensor_logger.service
sudo systemctl start sensor_logger.service

# Check timer status
systemctl list-timers --all

📊 To View Logs

journalctl -u rotate_csv.service
journalctl -u sensorlogger.service