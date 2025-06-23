# MQ-Sensors
Python code for RPI and MCP3008 to connect up to 8 sensors, log data, display, alert, and script configuration data. This example will use the MQ-135 Air Quality Sensor.

**Introduction**
The **MCP3008** is an 8-channel, 10-bit analog-to-digital converter (ADC) manufactured by MCP. It is designed to convert analog signals into digital data, enabling microcontrollers to process and interpret analog inputs. The MCP3008 communicates using the SPI (Serial Peripheral Interface) protocol, which ensures fast and reliable data transfer. This component is widely used in embedded systems for interfacing with sensors, potentiometers, and other analog devices.

This installation has **NOT** been set up (to install as a normal Python program with an icon and the environments set up automatically). This has been designed for lab deployment and data collection.

   **Reference websites**

    https://docs.cirkitdesigner.com/component/e3afbb86-da52-4bd2-b1c8-3669dd5bcd79/mcp3008

    https://www.allelcoelec.com/blog/A-Complete-Overview-of-the-MCP3008-ADC.html

**How to Use the MCP3008 in a Circuit**
   - Power Supply: Connect the VDD pin to a 3.3V or 5V power source, and connect the AGND and DGND pins to ground. (Set to the same level as the sensor uses)  In this project, the VREF and VDD are both 5V, as the sensor requires that level

   - Reference Voltage: Connect the VREF pin to a stable reference voltage (e.g., 3.3V or 5V). This determines the ADC's input range. 5V gives a resolution of 0-1023 and increases accuracy.

**SPI Connections:**
Physical:
  Connect the CS/SHDN pin to a GPIO pin on the microcontroller for chip select
  Connect the DIN pin to the SPI MOSI pin on the microcontroller
  Connect the DOUT pin to the SPI MISO pin on the microcontroller
  Connect the CLK pin to the SPI SCK pin on the microcontroller
  Analog Inputs: Connect up to 8 analog signals to the channel 0 – channel 7 pins

Microcontroller Configuration:
  SPI Configuration:  Configure the microcontroller's SPI interface to communicate with the MCP3008. 
                      Code config = SPI mode 0 (CPOL = 0, CPHA = 0)

**Wiring:**
Between the analog-digital-converter MCP3008 and the microcontroller Raspberry Pi Zero. Most Raspberry Pis have the same GPIO connection in the pinout diagram below. Therefore, you can use any RPi for this as needed.  For a simple reading for this project, the Zero with wireless is the most appropriate.

[MCP3008](https://microcontrollerslab.com/wp-content/uploads/2020/03/MCP3008-Simple-Connection-Diagram.jpg) 
Chip orientation is marked by a small semi-circular indentation on top of the physical chip to denote how the pins align with that indentation

[Raspberry Pi](https://pinout.xyz/)

Wire up as shown in the [wire schematic](https://www.instructables.com/Wiring-up-a-MCP3008-ADC-to-a-Raspberry-Pi-model-B-/) 

    MCP3008 pin 16 VDD  -> VDD        RPi pin 01  3.3V  (red)    
    MCP3008 pin 15 VREF -> VREF       RPi pin 01  3.3V  (red)    Should match sensor voltage used
    MCP3008 pin 14 AGND -> GND        RPi pin 05  GND (black)
    MCP3008 pin 13 CLK  -> SPi SCLK   RPi pin 23  (orange)
    MCP3008 pin 12 DOUT -> SPI MISO   RPi pin 21  (yellow)
    MCP3008 pin 11 DIN  -> SPI MOSI   RPi pin 19  (blue)
    MCP3008 pin 10 CS   -> GPIO 23    RPi pin 24  (violet) --Conf in code as Chip Select 0(off)/1(on)
    MCP3008 pin 09 DGND -> GND        RPi pin 05  (black)      Any of the GND pins will work

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
The MQ-135 measures ammonia, alcohol, benzene, smoke, carbon dioxide, etc. It operates at a 5V supply with 150mA consumption. Preheating for 5 minutes is required before the operation to obtain an accurate output.

Reminder: Needs approximately 5 minutes to warm up and should remain warm so it can be read at any time. 

MQ7 Air Quality Sensor | Detection of Carbon Monoxide (CO) - Very Dangerous at specific PPMs

MQ7 and MQ135 share the same pinouts - The links for one are reused for both.

![MQ135 Pin Configuration](![https://www.elprocus.com/wp-content/uploads/MQ135-Air-Quality-Sensor-Pin-Configuration-300x152.jpg])
   - VCC pin -> RPI pin 01 3.3V  (red)
   - GND pin -> RPi pin 06 GND   (black)
   - Do  pin -> unconnected

## **OPTIONAL**
![MQ7 Pin Configuration](![https://www.elprocus.com/wp-content/uploads/MQ135-Air-Quality-Sensor-Pin-Configuration-300x152.jpg])
   - VCC pin -> RPi Pin 01 3.3V  (red)  
   - GND pin -> RPi pin 06 GND   (black)
   - Do  pin -> unconnected
   - Ao  pin -> MCP3008 CH1-**pin 02**  (green)

![BMW/BMP280 Configuration](! ])
   - VIN	-> RPi Pin 01 (3.3V)         (red)
   - GND	-> RPi Pin 06 (GND)          (Black)
   - SCL	-> PPi Pin 05 (GPIO3 / SCL1) (Grey)
   - SDA	-> PPi Pin 03 (GPIO2 / SDA1) (purple)

### **Now that we've wired up, let us convert analog inputs to digital outputs**

---

### **INSTALL ON THE RASPBERRY PI**

If you do **RUN INTO AN ISSUE**, PLEASE retrace your steps and double-check your setups.
You may need to run the script from a virtual environment on your machine.  This installation has **NOT been set up (to install as a normal Python program with an icon and set up the environments automatically)."  This is designed for lab deployment and data collection.

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
  cd MQ135-AirQuality
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

7. Enable SPI on the Raspberry Pi (if not already enabled):
   ```sh
   sudo rapsi-config
   ```
   - Go to *Interfacing Options* > *SPI* > *Enable*

      - To test that the RPi is configured for SPI, you can execute the following command later or in a new terminal window
      - Open a Terminal
      ```sh
      ls /dev/
      ```
      - Check in the output that *spidev0.0* and *spidev0.1* are listed

   - If using remote access (another machine), you can enable SSH from here to save yourself a few steps.
   ```sh
   sudo raspi-config
   ```
      - Go to *Interfacing Options* > *SSH* > *Enable*
   
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

**NOTE:** If you are running headless or want to access remotely please use the remote instrucitons and what files to load onto the remote machine.

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
