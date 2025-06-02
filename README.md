# MQ135-AirQuality
Python code for RPI and MCP3008 to connect up to 8 sensor(s), data log, display, alert, configuration data.

**Introduction**
The **MCP3008** is an 8-channel, 10-bit analog-to-digital converter (ADC) manufactured by MCP. It is designed to convert analog signals into digital data, enabling microcontrollers to process and interpret analog inputs. The MCP3008 communicates using the SPI (Serial Peripheral Interface) protocol, which ensures fast and reliable data transfer. This component is widely used in embedded systems for interfacing with sensors, potentiometers, and other analog devices.

   **Reference websites**

    https://docs.cirkitdesigner.com/component/e3afbb86-da52-4bd2-b1c8-3669dd5bcd79/mcp3008

    https://www.allelcoelec.com/blog/A-Complete-Overview-of-the-MCP3008-ADC.html

**How to Use the MCP3008 in a Circuit**
   - Power Supply: Connect the VDD pin to a 3.3V or 5V power source, and connect the AGND and DGND pins to ground. (Set to same level as the sensor uses)  Inthis project the VREF and VDD are both 5V; as the sensor requires that level

   - Reference Voltage: Connect the VREF pin to a stable reference voltage (e.g., 3.3V or 5V). This determines the ADC's input range. 5V gives a resolution of 0-1023 and increases accuracy.

**SPI Connections:**
Connect the CS/SHDN pin to a GPIO pin on the microcontroller for chip select
Connect the DIN pin to the SPI MOSI pin on the microcontroller
Connect the DOUT pin to the SPI MISO pin on the microcontroller
Connect the CLK pin to the SPI SCK pin on the microcontroller
Analog Inputs: Connect up to 8 analog signals to the CH0–CH7 pins. Ensure the input voltage does not exceed VREF.

SPI Configuration: Configure the microcontroller's SPI interface to communicate with the MCP3008.    Code config = SPI mode 0 (CPOL = 0, CPHA = 0)

**Wiring:**
Between the MCP3008 and the microcontroller Raspberry Pi Zero.  Any of the Raspberry Pi's have the same GPIO connection used in the pinout diagram linked below.

[MCP3008](https://microcontrollerslab.com/wp-content/uploads/2020/03/MCP3008-Simple-Connection-Diagram.jpg) 
   Chip orientation is marked by a small semi-circular indentation on top of the physical chip to denote how the pins align with that indention

[Raspberry Pi](https://pinout.xyz/)

Wire up as shown in the [wire schematic](https://www.instructables.com/Wiring-up-a-MCP3008-ADC-to-a-Raspberry-Pi-model-B-/) 

    MCP3008 pin 16 VDD  -> VDD        RPi pin 02  5V  (red)    Can not exceed the VREF
    MCP3008 pin 15 VREF -> VREF       RPi pin 04  5V  (red)    Should match sensor voltage used
    MCP3008 pin 14 AGND -> GND        RPi pin 05  GND (black)
    MCP3008 pin 13 CLK  -> SPi SCLK   RPi pin 23  (orange)
    MCP3008 pin 12 DOUT -> SPI MISO   RPi pin 21  (yellow)
    MCP3008 pin 11 DIN  -> SPI MOSI   RPi pin 19  (blue)
    MCP3008 pin 10 CS   -> GPIO 23    RPi pin 24  (violet) --Conf in code as Chip Select 0(off)/1(on)
    MCP3008 pin 09 DGND -> GND        RPi pin 25  (black)

**DUE TO CURRENT DRAW OF 1 OR MORE SENSORS; THE VDD AND GND OF THE SENSOR WILL LIKELY NEED SEPERATE SUPPLIED POWER - THIS WILL ENSURE LOW NOISE AND CLEARER READINGS ALONG WITH OPTIONAL DECOUPLING CAPACITOR ON MCP3008 PIN 16**

## WILL ALSO ALLOW THE SENSORS CONSISTANT SUPPLY VOLTAGE TO RUN CONTINUOUSLY.  THEY NEED TO WARM UP (5 MINS) AND STAY WARM. SO THAT THEY CAN BE READ FROM AT ANY TIME.  THE PI IS SET TO SLEEP (LOWER CPU UTILIZATION BY PAUSING THE SCRIPT), UNTIL IT IS TIME TO RECORD THE NEXT READING.  THAT TIME WORKS FOR 1-8 SENSORS CONNECTED TO THE **MCP3008**.  Remember any of the inputs not connected to a sensor needs to be grounded.  That is how the MCP3008 skips that sensor reading.  This will can cause programmatic issues later, when reading in the data by the python scripting.

**Important Considerations and Best Practices**
   + **Input Voltage Range:** Ensure the input voltage does not exceed VREF to avoid damage or incorrect (noisy) readings

   + **Decoupling Capacitors:** Place a 0.1 µF ceramic capacitor close to the VDD pin to reduce noise
   
   + **SPI Speed:** Use an appropriate SPI clock speed (e.g., below 1 MHz) to ensure reliable communication. 
      Script is set up to define that at 500kHZ to cover up to 8 sensors read every 5 seconds, with plenty of time to spare.
   
   + **Unused Channels:** If not all channels are used, connect unused channels to ground to prevent floating inputs, this can also create 'noise". This also skip the reading of that channel.

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
   - Ensure the input signal is within the specified range (2.7V to VREF : max 5V)
   - Can optionally add a decoupling capacitor to the VDD Pin 16

---

**SAMPLE PROJECT**
   To test this project a Air Quality sensor that has an A0 (Analog output) that is connected to a channel 0 (Pin1) on the ADC Converter (MCP3008 above) that will change the value into a Digital number and calculate Percentage of that save value.

[MQ135 Air Quality Sensor](https://www.elprocus.com/mq135-air-quality-sensor/) | Detection of Volatile Organic Compound (VOC) - potential dangerous in certain PPMs

   An MQ135 air quality sensor is one type of MQ gas sensor used to detect, measure, and monitor a wide range of gases present in air like ammonia, alcohol, benzene, smoke, carbon dioxide, etc. It operates at a 5V supply with 150mA consumption. Preheating of 20 seconds is required before the operation, to obtain the accurate output.

![MQ135 Pin Configuration](![https://www.elprocus.com/wp-content/uploads/MQ135-Air-Quality-Sensor-Pin-Configuration-300x152.jpg])
   - VCC pin -> RPi pin 04 5V       (red)    Seperate from RPi
   - GND pin -> RPi pin 06 GND      (black)  Seperate from RPi
   - Do  pin -> unconnected
   - Ao  pin -> MCP3008 CH0-**pin 01**  (green)

<the MQ7 link below needs updated to the MQ7 datasheet; these two sensors happen to have the exact same pinouts.>

![MQ7 Pin Configuration](![https://www.elprocus.com/wp-content/uploads/MQ135-Air-Quality-Sensor-Pin-Configuration-300x152.jpg])
   - VCC pin -> RPi pin 04 5V       (red)    Seperate from RPi
   - GND pin -> RPi pin 06 GND      (black)  Seperate from RPi
   - Do  pin -> unconnected
   - Ao  pin -> MCP3008 CH1-**pin 02**  (green)

### **Now that we wired up lets convert analog inputs to digital outputs**

---

### **INSTALL ON THE RASPBERRY PI**

   If you do **NOT OR RAN INTO AN ISSUE** PLEASE retrace your steps and double-check your set ups.
   You may need to run the script form a virtual environment on your machine.  This installation has **NOT been set up (to install as a normal python program with an icon and set up the environments automatically.)"  This is designed for lab deployment and data collection.

Here are step-by-step instructions to **clone and install** the project into the default location /home/<your username>/MQ135-AirQuality/ on your Raspberry Pi:

1. Open a Terminal on your Raspberry Pi Zero (Where you attached the circuit and going to run the data collection)
   CTRL + ALT + T

2. Change to your home directory (optional, for clarity):
   '''sh
   cd ~
   '''

3. Clone the repository:
   '''sh
   git clone https://github.com/<your-username>/MQ135-AirQuality.git
   '''
   (Replace <your-username> with your actual GitHub username if needed.)

4. Move into the project directory:
   '''sh
   cd MQ135-AirQuality

5. (Optional) Create and activate a Python virtual environment:
   '''sh
   sudo python3 -m venv .venv
   source .venv/bin/activate
   '''

6. Install required Python packages:
   '''sh
   sudo pip install spidev matplotlib pandas
   '''

7. Enable SPI on the Raspberry Pi (if not already enabled):
   '''sh
   sudo rapsi-config
   '''
   - Go to *Interfacing Options* > *SPI* > *Enable*

      - to test that the RPi is configured for spi, you can execute the following command later or in a new terminal window
      - Open Terminal
      '''sh
      ls /dev/
      '''
      - Check in the output that *spidev0.0* and *spidev0.1* is listed

   - If using remote acess (another machine) You can enable SSH from here to save yourself a few steps.
   ```sh
   sudo raspi-config
   ```
      - Go to *Interfacing Options* > *SSH* > *Enable*
   
8. Let the PI and sensors power on for ~5 mins for the physical sensors to warm up, they will not accurately record data before then.  Then continue to next step when you are ready to record data.

9. Run the sensor logging script:
   '''sh
   python3 mq-sensors.py
   '''
   - This will begin recording data

**Now your project is set up in /home/<your username>/MQ135-AirQuality/ and ready to use!**
   You can run other scripts (like live_plot.py) to begin or *only on remote machine settings.py* from this directory as needed.

   - As enure you are recording data or to use it immediatley from the Raspberry Pi Zero you can run live_plot.py locally:

   '''sh
   python3 live-plot.py
   '''

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

3. **Note the path to your log file, if not the default install above**, e.g. `/home/<your rpi username>/MQ135-AirQuality/sensor_log.csv`

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
   - **Windows OS - Skip to "Install SSHFS:Windows Users" section below...**

2. **Create a mount point:**
   ```sh
   mkdir -p ~/pi_logs
   ```

3. **Mount the Pi’s directory using SSHFS:**
   ```sh
   sshfs <your username>@<PI_IP_ADDRESS>:/home/<your username>/MQ135-AirQuality ~/pi_logs
   ```
   - Replace `<PI_IP_ADDRESS>` with your Pi’s IP address
   - Use your actual Pi username

4. **Access the log file locally:**
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

**Install SSHFS:Windows Users**

Suggestion: Use ONE of the two below, to set up Windows SSHFS

-  [WinFsp + SSHFS-Win](https://github.com/billziss-gh/sshfs-win)

-  [Dokan SSHFS](https://github.com/dokan-dev/dokany) to mount SSHFS drives.

---

### **REMOTE MACHINE(S) INSTALLION OF FILES, CONFIGURE SETTINGS FOR REMOTE ACCESS**

**Now that you should be able to set up the configuration using 'settings.py' that will configure "live_plot.py" to the mounted SSHFS path (e.g., `~/pi_logs/sensor_log.csv`) *or windows location that you set up similar* and read the log file as if it were local! Continue with the instructions below for the python file setup**

1. You will need to create a folder to run scripts and store settings on your remote machine. Here is a suggestion, please alter as needed.

**NOTE:** You can either
   1. Clone the repository again ( if space is an issue you may delete the files you do not need)
   2. Creata a folder and copy the below below files into
      -  Linux:   /home/<your pi username>/MQ135-AirQuality/
      - Windows: C:/Users/<your windows username>/MQ135-AirQuality/

2. Copy these files from the RPI or if you cloned the repostory you can just keep the files listed below:

   configuration.json
   live_plot.py
   settings.py

3. Naviate to the folder you cloned, created and copied, or whichever the files are located.  Ensure you have Python3 and pip installed on this machine to be able to run them sucessfully.

4. Set up your remote instance

   '''sh
   python3 settings.py
   '''
   
   Choose SSHFS and input the information in the files you recorded or set up on the RPI Zero installation.

   Click 'Save Settings' and exit

5. When ready to view in realtime your results being collected

   '''sh
   python3 live_plot.py
   '''

## **YOU SHOULD NOW BE ABLE TO SEE THE DATA BEING COLLECTED**
   If you do **NOT OR RAN INTO AN ISSUE** PLEASE retrace your steps and double-check your set ups.
   You may need to run the script form a virtual environment on your machine.  This installation has **NOT been set up (to install as a normal python program with an icon and set up the environments automatically.)"  This is designed for lab deployment and data collection.
