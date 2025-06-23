# Various-Sensors
Python code for RPI and MCP3008 to connect up to 8 sensors, log data, display, alert, and script configuration data. This example will use the MQ-135 Air Quality Sensor.

**Introduction**
For the raspberry pi to be able to read various sensors, with limited number of pins available for the task.  We have to use sensors that adressable with the same number of wires, or add a middleware component that allows you to multiplex between the available connected sensors to that component.

The Raspberry Pi can utilize 2 middleware chips that use a chip select pin and will provide outputs from the connected sensors when polled by the Pi. In the example we are only using 1 chip MCP3008 chip select 0:0, but two can be used by utilizing the other chip select pin and 0:1 (and some slight program changes). Config can support a maximum of 16 sensors or other analog devices that output information on an Analog pin.

The **MCP3008** is an 8-channel, 10-bit analog-to-digital converter (ADC) manufactured by MCP. It is designed to convert analog signals into digital data, enabling microcontrollers to process and interpret analog inputs. The MCP3008 communicates using the SPI (Serial Peripheral Interface) protocol, which ensures fast and reliable data transfer. This component is widely used in embedded systems for interfacing with sensors, potentiometers, and other analog devices.

This installation has **NOT** been set up (to install as a normal Python program with an icon and the environments set up automatically). This has been designed for lab deployment and data collection.  We will set the Python script to run as a service upon start up of the RPi and will collect the data in the background after a 5 minute delayed start for some sensors to warm up.

   **Reference websites**

    https://docs.cirkitdesigner.com/component/e3afbb86-da52-4bd2-b1c8-3669dd5bcd79/mcp3008

    https://www.allelcoelec.com/blog/A-Complete-Overview-of-the-MCP3008-ADC.html

**How to Use the MCP3008 in a Circuit**
   - Power Supply: Connect the VDD pin to a 3.3V or 5V power source, and connect the AGND and DGND pins to ground. (Set to the same voltage level as the sensor uses)  In this project, the VREF and VDD are both 3.3V, as most of the sensors requires that level.

   - Reference Voltage: Connect the VREF pin to a stable reference voltage (e.g., 3.3V or 5V). This determines the ADC's input range. 3.3V give sa resolution of 0-123 675; 5V gives a resolution of 0-1023 and increased accuracy.

🔌 Power and Ground Connections
MCP3008 Pin	Label	Connected To	      Wire
         16	VDD	3.3V  (RPi Pin 01)	red
         15	VREF	3.3V  (RPi Pin 01)	red
         14	AGND	GND   (RPi Pin 06)	black
         09	DGND	GND   (RPi Pin 06)   black
🔁 SPI Connections
MCP3008 Pin	Signal	RPi GPIO	RPi Pin  SPI   Wire
         13	CLK	   GPIO 11	Pin 23   SCLK  orange
         12	DOUT	   GPIO 09	Pin 21   MISO  yellow
         11	DIN	   GPIO 10	Pin 19   MOSI  blue
         10	CS	      GPIO 08	Pin 24   CE0   Grey

Microcontroller Software Configuration (handled in the script):
  SPI Configuration:  Configure the microcontroller's SPI interface to communicate with the MCP3008. 
                      Code config = SPI mode 0 (CPOL = 0, CPHA = 0)

[Raspberry Pi](https://pinout.xyz/)

# *![*WIRING DIAGRAM**](/technical/RPi2w-MCP3008-sensors_Breadboard)

The Raspberry Pi is set to sleep mode, which reduces CPU utilization by pausing the script until it is time to record the next reading. This setup is effective for connecting between 1 to 8 sensors. **MCP3008**.

**Important Considerations and Best Practices**
   + **Input Voltage Range:** Ensure the input voltage does not exceed VREF to avoid damage or incorrect (noisy) readings

   + **Decoupling Capacitors:** Place a 0.1 µF ceramic capacitor close to the VDD pin to reduce noise
   
   + **SPI Speed:** Use an appropriate SPI clock speed (e.g., below 1 MHz) to ensure reliable communication. 
      The script is set up to define that at 500 kHz to cover up to 8 sensors read every 5 seconds, with plenty of time to spare.
   
   + **Unused Channels:** If all channels are not used, connect the unused channels to ground to prevent floating inputs. Ungrounded pins can also contribute to inaccurate readings. This also skips the reading of that channel, which helps with the Python scripting.

---

**# Troubleshooting and FAQs**
**Common Issues and Solutions**

**1. No Output or Incorrect Readings:**
   - Verify all connections, especially SPI pins and power supply
   - Ensure the CS/SHDN pin is correctly toggled during communication.  
         This is done by programming the RPI's connected pin into a high state.
   - Check that the SPI mode is set to mode 0 (CPOL = 0, CPHA = 0)
         This is done in the mq-sensors.py SPI configuration section

**2. Floating or Noisy Readings:**
   - Ensure **unused** analog input channels are connected to ground
   - Use proper shielding and grounding techniques to minimize noise

**3. Low Accuracy or Resolution:**
   - Verify that the reference voltage (VREF) is stable and noise-free
   - Ensure the input signal is within the specified range (2.7V to VREF: max 5V)
   - Can optionally add a decoupling capacitor to the VDD Pin 16

---

**SAMPLE PROJECT**
   To test this project, an Air Quality sensor that has an A0 (Analog output) that is connected to channel 0 (Pin1) on the ADC Converter (MCP3008 above) that will change the value into a Digital number and calculate the Percentage of that measured value.  Therefore, the sensor resolution is the sample size of the analog voltage * (Sensor max measure ppm/sample size) = 

These air quality sensors are but two MQ sensors used to detect, measure, and monitor a wide range of gases present in the air.

[MQ135 Air Quality Sensor](https://www.elprocus.com/mq135-air-quality-sensor/) | Detection of Volatile Organic Compound (VOC) - potentially dangerous in certain PPMs
The MQ-135 measures ammonia, alcohol, benzene, smoke, carbon dioxide, etc. It operates at a 3.3 - 5V supply with 150mA consumption. Preheating for 5 minutes is required before the operation to obtain an accurate output.

MQ007 Air Quality Sensor | Detection of Carbon Monoxide (CO) - Very Dangerous at specific PPMs

MQ7 and MQ135 share the same pinouts - The links for one are reused for both.

![MQ Sensors Pin Configuration](![https://www.elprocus.com/wp-content/uploads/MQ135-Air-Quality-Sensor-Pin-Configuration-300x152.jpg])

🔁 I2C Connections
BME/BMP280  Pin	Signal	RPi Pin	I2C   Wire
            01	   VIN	   Pin 01         red
            02	   GND	   Pin 06         black
            03	   SCL	   Pin 05   SCL1  purple
            04	   SDA      Pin 02   SDA1  grey

### **Now that we've wired up, let us convert Various sensor inputs to digital outputs**

---

### **INSTALL ON THE RASPBERRY PI**

If you do **RUN INTO AN ISSUE**, PLEASE retrace your steps and double-check your setups.
You may need to run the script from a virtual environment on your machine.    This is designed for lab deployment and data collection.

Here are step-by-step instructions to **clone and install** the project into the default location */home/**Rpi username*/MQ-Sensors/* on your Raspberry Pi:

1. Open a Terminal on your Raspberry Pi Zero (Where you attached the circuit and are going to run the data collection)
   CTRL + ALT + T
 
2. Change to your home directory (optional, for clarity):
   ```sh
   cd ~
   ```

3. Clone the repository:
   ```sh
   git clone https://github.com/OsirianOne71/MQ-Sensors.git
   ```

4. Move into the project directory:
  ```sh
  cd sensors-pi
  ```

5. (Optional) Create and activate a Python virtual environment:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

6. Install required Python packages:
   ```sh
   sudo pip install spidev matplotlib pandas
   ```

7. Enable I²C and SPI via raspi-config:
   ```sh
   sudo rapsi-config
   ```
   # Interface Options -> Enable I2C Go to *Interfacing Options* > *I2C* > *Enable*
   # Interface Options -> Enable SPI Go to *Interfacing Options* > *SPI* > *Enable*
   # Interface Options -> Enable SSH Go to *Interfacing Options* > *SSH* > *Enable*

   - To test that the RPi is configured for SPI, you can execute the following command later or in a new terminal window
      - Open a Terminal
      ```sh
      ls /dev/
      ```
      - Check in the output that *spidev0.0* and/or *spidev0.1* are listed
   
8. Let the PI and sensors power on for ~5 mins for the physical sensors to warm up; they will not accurately record data before then.  Then, continue to the next step when you are ready to record data.

9. Run the sensor logging script:
   ```sh
   python3 mq-sensors.py
   ```
   This will begin recording data

Now your project is set up in */home/**RPI_USERNAME**/MQ-Sensors/* and ready to use!
   To ensure you are recording data or to use it immediately from the Raspberry Pi Zero, you can run live_plot.py locally. If you want to be able to run the script on a remote machine and/or run the Raspberry Pi Zero headless, then you can follow the instructions to set up on a remote machine further below.

   ```sh
   python3 live-plot.py
   ```

To recover from a power loss, Brown out etc.  Set the script to run as a systemd service when the Pi Zero 2W boots.

1. Make sure your script is executable and uses the correct Python shebang
At the top of your script (e.g., weatherinfo.py), add:

`#!/usr/bin/env python3`

Then make it executable:

`chmod +x /home/pi/MQ-Sensors/weatherinfo.py`

2. Create a systemd service file
Create a new service file, for example:

`sudo nano /etc/systemd/system/sensorlogger.service`

Paste the following (edit paths as needed):
`[Unit]
Description=MQ Sensor Logger
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/MQ-Sensors/weatherinfo.py
WorkingDirectory=/home/pi/MQ-Sensors
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target`

3. Enable and start the service

`sudo systemctl daemon-reload
sudo systemctl enable sensorlogger.service
sudo systemctl start sensorlogger.service`

Check status and logs

`sudo systemctl status sensorlogger.service
journalctl -u sensorlogger.service -f`



---

### **ENABLING SSH FOR REMOTE LOG ACCESS**

### **On the Raspberry Pi Zero (where the log is):**

1. **Make sure SSH is enabled:**
   ```sh
   sudo raspi-config
   ```
   - Go to *Interfacing Options* > *SSH* > *Enable*.

2. **Find the Pi’s IP address:**
   ```sh
   hostname -I
   ```

3. **Note the path to your log file, if not the default install above**, e.g., `/home/**rpi-username**/MQ-Sensors/sensor_log.csv`

### **You will need all this information along with your **password** to set up the **remote machine**

---

### **On the Remote Machine (Linux/macOS):**

1. **Install SSHFS:**

   - **Ubuntu/Debian:**
     ```sh
     sudo apt update
     sudo apt install sshfs
     ```
   - **macOS (with Homebrew):**
     ```sh
     brew install sshfs
     ```
   - **Windows OS - Skip to "Install SSHFS: Windows Users" section below...**

2. **Create a mount point:**
   ```sh
   mkdir -p ~/pi_logs
   ```

3. **Mount the Pi’s directory using SSHFS:**
   ```sh
   sshfs <RPI_USERNAME>@<PI_IP_ADDRESS>:/home/your-rpi-username/MQ-Sensors ~/pi_logs
   ```
   - **Replace** `<RPI-USERNAME>` with your Raspberry Pi Username
   - Replace `<PI_IP_ADDRESS>` with your Pi’s IP address

5. **Access the log file locally:**
   - The file will now be available at `~/pi_logs/sensor_log.csv` on your remote machine.

---

### **To Unmount When Done:**

- **Linux:**
  ```sh
  fusermount -u ~/pi_logs
  ```
- **macOS:**
  ```sh
  umount ~/pi_logs
  ```

**Install SSHFS: Windows Users**

Suggestion: Use ONE of the two below to set up Windows SSHFS

-  [WinFsp + SSHFS-Win](https://github.com/billziss-gh/sshfs-win)

-  [Dokan SSHFS](https://github.com/dokan-dev/dokany) to mount SSHFS drives.

---

### **REMOTE MACHINE(S) INSTALLATION OF FILES, CONFIGURE SETTINGS FOR REMOTE ACCESS**

**Now that you should be able to set up the configuration using 'settings.py' that will configure "live_plot.py" to the mounted SSHFS path (e.g., `~/pi_logs/sensor_log.csv`) *or windows location that you set up similarly* and read the log file as if it were local! Continue with the instructions below for the Python file setup**

1. You will need to create a folder to run scripts and store settings on your **remote machine**. Here is a suggestion, please alter as needed.

**NOTE:** You can either
   1. Clone the repository again ( if space is an issue, you may delete the files you do not need)
   2. Create a folder and copy the files below into it
      - Linux:   */home/**rpi-username**/MQ-Sensors/*
      - Windows: *C:/Users/**windows-username**/MQ-Sensors/*

2. Copy these files from the RPI, or if you cloned the repository, you can just keep the files listed below:

   configuration.json
   live_plot.py
   settings.py

3. Naviate to the folder you cloned, created and copied, or whichever the files are located.  Ensure you have Python3 and pip installed on this machine to be able to run them sucessfully.

4. Set up your remote instance

   ```sh
   python3 settings.py
   ```
   Choose SSHFS and input the information in the files you recorded or set up on the RPI Zero installation.
   *path or folder field* needs to be fqdn /home/...

   Click 'Save Settings' and exit

6. When ready to view in real-time

   ```sh
   python3 live_plot.py
   ```

## **YOU SHOULD NOW BE ABLE TO SEE THE DATA BEING COLLECTED**
If you do **encounter an ISSUE**, PLEASE retrace your steps and double-check your setups.
You may need to run the script from a virtual environment on your machine.  
This installation has **NOT** been set up (to install as a normal Python program with an icon and the environments set up automatically). This has been designed for lab deployment and data collection.


THINGS TO NOTE FROM OTHER PROJECTS:

https://cdn.sparkfun.com/assets/b/b/b/3/4/MQ-7.pdf
https://www.tastethecode.com/mq7-carbon-monoxide-sensor-done-the-right-way
