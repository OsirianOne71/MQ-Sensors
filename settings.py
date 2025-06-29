#! /usr/bin/env python3
# This script provides a GUI for configuring system settings related to sensor logging and Dashboard display.
import ttkbootstrap as tb
from ttkbootstrap.constants import LEFT, RIGHT, TOP, BOTTOM, X, Y, BOTH, W, E, N, S
import tkinter as tk
import json
import os
import pytz
import requests
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog

CONFIG_FILE = "configuration.json"

class SettingsWindow(tb.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("System Settings")
        self.geometry("400x700")  # Increased height
        self.resizable(False, False)

        self.conn_type = tk.StringVar(value="Local")
        self.local_path = tk.StringVar()
        self.ssh_host = tk.StringVar()
        self.ssh_user = tk.StringVar()
        self.ssh_path = tk.StringVar()
        self.sshfs_mount = tk.StringVar()
        self.ssh_password = tk.StringVar()
        self.screen_duration = tk.IntVar(value=5)
        self.zip_code = tk.StringVar()
        self.time_zone = tk.StringVar(value="America/New_York")
        self.city_state = tk.StringVar()
        self.latitude = tk.StringVar()
        self.longitude = tk.StringVar()
        self.tzdb_username = tk.StringVar()
        self.tzdb_apikey = tk.StringVar()
        self.units = tk.StringVar()

        self.load_settings()

        # --- Dashboard/Weather fields at the top ---

        # Row for Zip Code and City, State
        zip_city_frame = tb.Frame(self)
        zip_city_frame.pack(anchor="w", padx=10, pady=(4, 0), fill="x")

        tb.Label(zip_city_frame, text="Zip Code:").pack(side="left")
        tb.Entry(zip_city_frame, textvariable=self.zip_code, width=10).pack(side="left", padx=(2, 10))

        tb.Label(zip_city_frame, text="City, State:").pack(side="left")
        tb.Entry(zip_city_frame, textvariable=self.city_state, width=16).pack(side="left", padx=(2, 0))

        tb.Button(self, text="Lookup Location", command=self.lookup_location).pack(anchor="w", padx=20, pady=(0, 8))

        # Row for Latitude and Longitude
        latlong_frame = tb.Frame(self)
        latlong_frame.pack(anchor="w", padx=10, pady=(4, 0), fill="x")

        tb.Label(latlong_frame, text="Latitude:").pack(side="left")
        tb.Entry(latlong_frame, textvariable=self.latitude, width=14).pack(side="left", padx=(2, 10))

        tb.Label(latlong_frame, text="Longitude:").pack(side="left")
        tb.Entry(latlong_frame, textvariable=self.longitude, width=14).pack(side="left", padx=(2, 0))

        # Time Zone and Screen Cycle Time below
        tb.Label(self, text="Time Zone:").pack(anchor="w", padx=10, pady=(8, 0))
        self.time_zone_combo = tb.Combobox(self, textvariable=self.time_zone, values=sorted(pytz.all_timezones), width=30)
        self.time_zone_combo.pack(anchor="w", padx=20, pady=(0, 4))

        # Screen Cycle Time and Units side by side
        cycle_units_frame = tb.Frame(self)
        cycle_units_frame.pack(anchor="w", padx=10, pady=(4, 8), fill="x")

        tb.Label(cycle_units_frame, text="Screen Cycle Time (sec):").pack(side="left")
        tb.Entry(cycle_units_frame, textvariable=self.screen_duration, width=10).pack(side="left", padx=(2, 12))

        tb.Label(cycle_units_frame, text="Units:").pack(side="left")
        tb.Combobox(cycle_units_frame, textvariable=self.units, values=["F", "C", "Imperial"], width=10).pack(side="left", padx=(2, 0))

        tb.Button(self, text="Open configuration.json", command=self.open_config).pack(anchor="w", padx=20, pady=10)

        # --- Connection Type selection (must be after load_settings) ---
        tb.Label(self, text="Connection Type:").pack(anchor="w", padx=10, pady=(10, 0))
        for mode in ["Local", "Stream over SSH", "SSHFS"]:
            tb.Radiobutton(self, text=mode, variable=self.conn_type, value=mode, command=self.update_fields).pack(anchor="w", padx=20)

        # Local path
        self.local_frame = tb.Frame(self)
        tb.Label(self.local_frame, text="Log File Path:").pack(side="left")
        tb.Entry(self.local_frame, textvariable=self.local_path, width=30).pack(side="left", padx=5)
        tb.Button(self.local_frame, text="Browse", command=self.browse_local).pack(side="left")

        self.ssh_frame = tb.Frame(self)
        tb.Label(self.ssh_frame, text="SSH Host:").grid(row=0, column=0, sticky="w")
        tb.Entry(self.ssh_frame, textvariable=self.ssh_host, width=20).grid(row=0, column=1, padx=5)
        tb.Label(self.ssh_frame, text="SSH User:").grid(row=1, column=0, sticky="w")
        tb.Entry(self.ssh_frame, textvariable=self.ssh_user, width=20).grid(row=1, column=1, padx=5)
        tb.Label(self.ssh_frame, text="SSH Password:").grid(row=2, column=0, sticky="w")
        tb.Entry(self.ssh_frame, textvariable=self.ssh_password, width=20, show="*").grid(row=2, column=1, padx=5)
        tb.Label(self.ssh_frame, text="Remote Path:").grid(row=3, column=0, sticky="w")
        tb.Entry(self.ssh_frame, textvariable=self.ssh_path, width=30).grid(row=3, column=1, padx=5)

        self.sshfs_frame = tb.Frame(self)
        tb.Label(self.sshfs_frame, text="SSHFS Mount Point:").pack(side="left")
        tb.Entry(self.sshfs_frame, textvariable=self.sshfs_mount, width=30).pack(side="left", padx=5)

        self.update_fields()  # <-- Now it's safe to call!

        # TimeZoneDB fields at the bottom, side by side
        tzdb_frame = tb.Frame(self)
        tzdb_frame.pack(side="bottom", fill="x", padx=10, pady=(8, 8))

        tb.Label(tzdb_frame, text="TimeZoneDB Username:").pack(side="left")
        tb.Entry(tzdb_frame, textvariable=self.tzdb_username, width=18).pack(side="left", padx=(10, 12))

        tb.Label(tzdb_frame, text="API Key:").pack(side="left")
        tb.Entry(tzdb_frame, textvariable=self.tzdb_apikey, width=24, show="*").pack(side="left", padx=(10, 0))

        tb.Button(self, text="Save Settings", command=self.save_settings).pack(side="bottom", pady=2)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.update_fields()  # <-- Move here, after all frames are created


    def load_settings(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
            self.conn_type.set(config.get("connection_type", "Local"))
            self.local_path.set(config.get("local_path", ""))
            self.ssh_host.set(config.get("ssh_host", ""))
            self.ssh_user.set(config.get("ssh_user", ""))
            self.ssh_path.set(config.get("ssh_path", ""))
            self.sshfs_mount.set(config.get("sshfs_mount", ""))
            self.ssh_password.set(config.get("ssh_password", ""))
            # Load new fields
            self.screen_duration.set(config.get("screen_duration", 5))
            self.zip_code.set(config.get("zip_code", ""))
            self.time_zone.set(config.get("time_zone", "America/New_York"))
            self.city_state.set(config.get("city_state", ""))
            self.latitude.set(config.get("latitude", ""))
            self.longitude.set(config.get("longitude", ""))
            self.tzdb_username.set(config.get("tzdb_username", "osirianone"))
            self.tzdb_apikey.set(config.get("tzdb_apikey", "LV6KGE90II1O"))
            self.units.set(config.get("units", "F"))  # Default to Fahrenheit
        else:
            # Create a default config file if it does not exist
            config = {
                "connection_type": "Local",
                "local_path": "",
                "ssh_host": "",
                "ssh_user": "",
                "ssh_path": "",
                "sshfs_mount": "",
                "ssh_password": "",
                "screen_duration": 5,
                "zip_code": "",
                "time_zone": "America/New_York",
                "city_state": "",
                "latitude": "",
                "longitude": "",
                "tzdb_username": "",
                "tzdb_apikey": "",
                "units": "F"  # Default to Fahrenheit
            }
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=2)
            # Set defaults in the GUI
            self.conn_type.set("Local")
            self.local_path.set("")
            self.ssh_host.set("")
            self.ssh_user.set("")
            self.ssh_path.set("")
            self.sshfs_mount.set("")
            self.ssh_password.set("")
            self.screen_duration.set(5)
            self.zip_code.set("")
            self.time_zone.set("America/New_York")
            self.city_state.set("")
            self.latitude.set("")
            self.longitude.set("")
            self.tzdb_username.set("")
            self.tzdb_apikey.set("")
            self.units.set("F")  # Default to Fahrenheit

    def update_fields(self):
        self.local_frame.pack_forget()
        self.ssh_frame.pack_forget()
        self.sshfs_frame.pack_forget()
        if self.conn_type.get() == "Local":
            self.local_frame.pack(anchor="w", padx=20, pady=5)
        elif self.conn_type.get() == "Stream over SSH":
            self.ssh_frame.pack(anchor="w", padx=20, pady=5)
        elif self.conn_type.get() == "SSHFS":
            self.sshfs_frame.pack(anchor="w", padx=20, pady=5)

    def browse_local(self):
        path = filedialog.askopenfilename(title="Select Log File")
        if path:
            self.local_path.set(path)

    def open_config(self):
        if os.path.exists(CONFIG_FILE):
            os.startfile(CONFIG_FILE)
        else:
            Messagebox.show_error("Error", f"{CONFIG_FILE} not found.", parent=self)

    def save_settings(self):
        config = {
            "connection_type": self.conn_type.get(),
            "local_path": self.local_path.get(),
            "ssh_host": self.ssh_host.get(),
            "ssh_user": self.ssh_user.get(),
            "ssh_path": self.ssh_path.get(),
            "sshfs_mount": self.sshfs_mount.get(),
            "ssh_password": self.ssh_password.get(),
            # Save new fields
            "screen_duration": self.screen_duration.get(),
            "zip_code": self.zip_code.get(),
            "time_zone": self.time_zone.get(),
            "city_state": self.city_state.get(),
            "latitude": self.latitude.get(),
            "longitude": self.longitude.get(),
            "tzdb_username": self.tzdb_username.get(),
            "tzdb_apikey": self.tzdb_apikey.get(),
            "units": self.units.get(),
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        Messagebox.show_info("Saved", "Settings saved to configuration.json", parent=self)
        self.destroy()
        self.master.destroy()  # <-- Add this line to close the hidden root window
        if self.time_zone.get() not in pytz.all_timezones:
            self.time_zone.set("America/New_York")

    def on_close(self):
        self.destroy()
        self.master.destroy()

    def lookup_location(self):
        zip_code = self.zip_code.get().strip()
        if not zip_code:
            Messagebox.show_error("Error", "Please enter a ZIP code.", parent=self)
            return
        try:
            resp = requests.get(f"http://api.zippopotam.us/us/{zip_code}", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                city = data['places'][0]['place name']
                state = data['places'][0]['state abbreviation']
                lat = data['places'][0]['latitude']
                lng = data['places'][0]['longitude']
                self.city_state.set(f"{city}, {state}")
                self.latitude.set(lat)
                self.longitude.set(lng)

                # After setting self.latitude and self.longitude
                lat = self.latitude.get()
                lng = self.longitude.get()
                apikey = self.tzdb_apikey.get()
                if lat and lng and apikey:
                    try:
                        tz_resp = requests.get(
                            f"http://api.timezonedb.com/v2.1/get-time-zone?key={apikey}&format=json&by=position&lat={lat}&lng={lng}",
                            timeout=5
                        )
                        if tz_resp.status_code == 200:
                            tz_data = tz_resp.json()
                            zone = tz_data.get("zoneName", "")
                            if zone:
                                self.time_zone.set(zone)
                    except Exception as e:
                        Messagebox.show_error("Error", f"Failed to lookup time zone: {e}", parent=self)
            else:
                Messagebox.show_error("Error", f"ZIP code {zip_code} not found.", parent=self)
        except Exception as e:
            Messagebox.show_error("Error", f"Failed to lookup location: {e}", parent=self)

if __name__ == "__main__":
    root = tb.Window(themename="darkly")  # or "superhero", "cyborg", etc.
    root.withdraw()  # Hide the root window
    SettingsWindow(root)
    root.mainloop()