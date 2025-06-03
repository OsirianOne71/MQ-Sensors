# SSHFS-Win & WinFsp Installation Guide (Windows)

This guide explains how to install **WinFsp** and **SSHFS-Win** on Windows, allowing you to mount remote directories (such as from a Raspberry Pi) over SSH as local drives.

---

## 1. Install WinFsp & SSHFS-Win
- WinFsp is a Windows File System Proxy required for SSHFS-Win.
- SSHFS-Win allows you to mount remote filesystems over SSH.

### Option A: Using `winget` (recommended for Windows 10/11)

Open **Command Prompt** or **PowerShell** as Administrator and run:

```sh
winget install SSHFS-Win.SSHFS-Win
```

### Option B: Manual Download

- Download the latest WinFsp installer from:  
  [https://github.com/winfsp/winfsp/releases](https://github.com/winfsp/winfsp/releases)
- Run the installer and follow the prompts to complete installation.

- Download the latest SSHFS-Win installer from:  
  [https://github.com/winfsp/sshfs-win/releases](https://github.com/winfsp/sshfs-win/releases)
- Run the installer and follow the prompts.

---

## 2. Mount a Remote Directory

After installation, you can mount a remote directory using Windows Explorer or the command line.

### **A. Using Windows Explorer**

1. Open "This PC" in File Explorer.
2. Click "Map network drive".
3. Choose a drive letter.
4. In the "Folder" field, enter:
   ```
   \\sshfs\pi@raspberrypi.local\home\pi\MQ-Sensors
   ```
   - Replace `pi` with your username and `raspberrypi.local` with your Pi's hostname or IP
   - Adjust the remote path as needed
5. Click "Finish" and enter your SSH password when prompted

### **B. Using Command Line**
   ```
   net use X: \\sshfs\<pi>@<raspberrypi.local>\home\pi\MQ-Sensors
   ```
   - Replace `X:` with your desired drive letter.
   - Replace `pi` with your username and `raspberrypi.local` with your Pi's hostname or IP
   - Adjust the remote path as needed

---

## 3. More Information

For advanced usage, troubleshooting, and options, see the official documentation:  
[https://github.com/winfsp/sshfs-win](https://github.com/winfsp/sshfs-win)

---

**Now you can access your Raspberry Pi files (like `sensor_log.csv`) as if they were on your Windows machine!**