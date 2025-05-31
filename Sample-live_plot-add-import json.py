import json
import os

CONFIG_FILE = "configuration.json"

# Load settings from configuration.json
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
else:
    config = {}

# Use settings from config
connection_type = config.get("connection_type", "Local")
local_path = config.get("local_path", "sensor_log.csv")
ssh_host = config.get("ssh_host", "")
ssh_user = config.get("ssh_user", "")
ssh_path = config.get("ssh_path", "")
sshfs_mount = config.get("sshfs_mount", "")

# Example: set LOG_FILE based on connection type
if connection_type == "Local":
    LOG_FILE = local_path
elif connection_type == "SSHFS":
    LOG_FILE = os.path.join(sshfs_mount, os.path.basename(local_path))
elif connection_type == "Stream over SSH":
    # For streaming, you would implement logic to read the file over SSH
    LOG_FILE = None  # Placeholder
else:
    LOG_FILE = "sensor_log.csv"

# ...rest of your plotting code...