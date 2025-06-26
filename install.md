🧪 Deployment Steps

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