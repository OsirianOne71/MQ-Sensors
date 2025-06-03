## How to configure Stream over SSH

**Raspberry Pi to appear in Network devices**
    ```sh
    sudo apt install wsdd
    ```

**Raspberry Pi share folders to windows using Samba**
    https://pimylifeup.com/raspberry-pi-samba/

1. check for updates
    ```sh
    sudo apt update && sudo apt upgrade -y
    ```

2. Install Samba
    ```sh
    sudo apt install samba samba-common-bin
    ```

3. Modify Samba config
    ```sh
    sudo nano /etc/samba/smb.conf
    ```

4. At the bottom of the file
 -Set the share in smb.conf as below:

    [mqlogging]
    path = /home/<PI USERNAME>/MQ-Sensors
    Comment = home user mqsensors shared folder
    Browseable = yes
    Writeable = yes
    public = no

5. Save the file using CTL + O, Then exit using CTRL + X

6. Set your Pi username as a smb user
    ```sh
    sudo smbpasswd -a <USERNAME>
    ```

7. You will be prompted for the following:
    New SMB password:
    Retype new SMB password:

    *Suggestion: Set up the same as your Pi username to start with*

    If the response is *Added user USERNAME*, then you can continue

8. Restart SAMBA service
    ```sh
    sudo systemctl restart smbd
    ```

---

**Set up a mapped drive in Windows**

1. Launch **File Explorer** > Right Click on **Network** > Choose **Map Network Drive**

2. Fill in the network mapping window
    - Choose a Drive letter that you prefer to use for this task
    - Folder enter as follows:
        *\\<IP_ADDRESS>\MQ-Sensors*
    
    - Replace <IP_ADDRESS> with your Raspberry Pi IP ADDRESS
        Folder name is as we set it up in smb.conf    
    - Click the **Finish** button

3. Enter your Raspberry Pi Credentials
    - <RPI_USERNAME>
    - <Samba password> that was set up installing samba>

4. That should now open a file folder showing the contents of MQ-Sensors

5. On Remote machine run
    ```sh
    python3 settings.py
    ```

    Choose **Stream over SSH**
    Enter all the information
    - ssh_host = <RPI_IP_ADDRESS>
    - ssh_user = <RPI SMB user name>
    - ssh_path = <full path to the folder>
                /home/<PI_USERNAME>/MQ-Sensors
    - ssh_password = <RPI USER_PASSWORD>
                Not your samba password unless you set it as the same
    - Click **Save Settings"

6. You should be set up to begin logging and on the remote computer launch your graphs using

    ```sh
    python3 live_plot.py
    ```
