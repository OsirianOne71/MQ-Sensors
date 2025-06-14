import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

CONFIG_FILE = "configuration.json"

class SettingsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("System Settings")
        self.geometry("400x320")  # Set a fixed size for the window
        self.resizable(False, False)

        self.conn_type = tk.StringVar(value="Local")
        self.local_path = tk.StringVar()
        self.ssh_host = tk.StringVar()
        self.ssh_user = tk.StringVar()
        self.ssh_path = tk.StringVar()
        self.sshfs_mount = tk.StringVar()
        self.ssh_password = tk.StringVar()

        # Load settings if config file exists
        self.load_settings()

        # Connection type selection
        ttk.Label(self, text="Connection Type:").pack(anchor="w", padx=10, pady=(10,0))
        for mode in ["Local", "Stream over SSH", "SSHFS"]:
            ttk.Radiobutton(self, text=mode, variable=self.conn_type, value=mode, command=self.update_fields).pack(anchor="w", padx=20)

        # Local path
        self.local_frame = ttk.Frame(self)
        ttk.Label(self.local_frame, text="Log File Path:").pack(side="left")
        ttk.Entry(self.local_frame, textvariable=self.local_path, width=30).pack(side="left", padx=5)
        ttk.Button(self.local_frame, text="Browse", command=self.browse_local).pack(side="left")
        self.local_frame.pack(anchor="w", padx=20, pady=5)

        # SSH fields
        self.ssh_frame = ttk.Frame(self)
        ttk.Label(self.ssh_frame, text="SSH Host:").grid(row=0, column=0, sticky="w")
        ttk.Entry(self.ssh_frame, textvariable=self.ssh_host, width=20).grid(row=0, column=1, padx=5)
        ttk.Label(self.ssh_frame, text="SSH User:").grid(row=1, column=0, sticky="w")
        ttk.Entry(self.ssh_frame, textvariable=self.ssh_user, width=20).grid(row=1, column=1, padx=5)
        ttk.Label(self.ssh_frame, text="SSH Password:").grid(row=2, column=0, sticky="w")
        ttk.Entry(self.ssh_frame, textvariable=self.ssh_password, width=20, show="*").grid(row=2, column=1, padx=5)
        ttk.Label(self.ssh_frame, text="Remote Path:").grid(row=3, column=0, sticky="w")
        ttk.Entry(self.ssh_frame, textvariable=self.ssh_path, width=30).grid(row=3, column=1, padx=5)
        
        # SSHFS fields
        self.sshfs_frame = ttk.Frame(self)
        ttk.Label(self.sshfs_frame, text="SSHFS Mount Point:").pack(side="left")
        ttk.Entry(self.sshfs_frame, textvariable=self.sshfs_mount, width=30).pack(side="left", padx=5)

        # Config file link
        ttk.Button(self, text="Open configuration.json", command=self.open_config).pack(anchor="w", padx=20, pady=10)

        self.update_fields()

        # Save button (move to bottom)
        ttk.Button(self, text="Save Settings", command=self.save_settings).pack(side="bottom", pady=10)


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
        else:
            # Create a default config file if it does not exist
            config = {
                "connection_type": "Local",
                "local_path": "",
                "ssh_host": "",
                "ssh_user": "",
                "ssh_path": "",
                "sshfs_mount": "",
                "ssh_password": ""
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
            messagebox.showerror("Error", f"{CONFIG_FILE} not found.", parent=self)

    def save_settings(self):
        config = {
            "connection_type": self.conn_type.get(),
            "local_path": self.local_path.get(),
            "ssh_host": self.ssh_host.get(),
            "ssh_user": self.ssh_user.get(),
            "ssh_path": self.ssh_path.get(),
            "sshfs_mount": self.sshfs_mount.get(),
            "ssh_password": self.ssh_password.get(),
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        messagebox.showinfo("Saved", "Settings saved to configuration.json", parent=self)
        self.destroy()
        self.master.destroy()  # <-- Add this line to close the hidden root window

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    SettingsWindow(root)
    root.mainloop()