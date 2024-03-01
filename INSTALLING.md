## Installing pyEFIS and FIX-Gateway
The following instructions are specific to the latest 64bit Raspbian bullseye and may not work on other versions or operating systems.

### Install the latest updates
Open a terminal window and run:
```
sudo apt update
sudo apt dist-upgrade -y
```

### Install snapd
Install snapd
```
sudo apt install -y snapd
```

### Reboot
You must reboot before proceeding
```
sudo reboot
```

### Install snap core
Install core snap to update snapd
```
sudo snap install core
```

### Install pyEFIS
Install the pyefis snap
```
sudo snap install pyefis
```

### Install FIX-Gateway
Install the fixgateway snap
```
sudo snap install fixgateway
```

### Requirements for some hardware
Depending on what hardware you will be interfacing you may need to perform the steps in this section. It will not hurt to do them even if you don't use this hardware so you might just want to do them anyway and have your system prepared for future changes.
<br>
Snaps run in an isolated container and do not have un-restricted access to your system. Depending on what hardware you are using you might need to grant the fixgateway snap permissions to access the hardware.
<br>

#### CAN bus
If you are using CAN, allow fixgateway access to CAN:
```
snap connect fixgateway:can-bus snapd
```

#### Serial ports
If you are using serial ports to access your hardware, allow fixgateway to access serial ports.

Add yourself to the dialout group:
```
sudo usermod -a -G dialout ${USER}
newgrp dialout
```

Enable hotplug option in snapd:
```
sudo snap set system experimental.hotplug=true
```

Restart snapd to apply the hotplug change:
```
sudo systemctl restart snapd.service
```

These next few steps are specific to your system so you will need to run commands to get some data and then use that data in other commands.

List serial port slots/plugs:
```
snap interface serial-port --attrs
```

In the output you are looking for the name of your serial port.
Now run command using that name replacing serial-name-here:
```
sudo snap connect fixgateway:serial-port snapd:serial-name-here
```

### Setup auto start
This will setup automatic start for pyefis and fixgateway.

#### Auto start fixgateway

You may need to first create the systemd/user directory:
```
mkdir -p ~/.config/systemd/user/
```

Copy the fixgateway systemd unit file:
```
cp /snap/fixgateway/current/extras/fixgateway.service ~/.config/systemd/user/
```

If you want to change the config file used edit the file you just copied and make that change.<br>

Enable automatic start of fixgateway
```
systemctl --user enable fixgateway.service
```

Start Fix Gateway:
```
systemctl --user start fixgateway.service
```

#### Auto start pyefis
Copy the pyefis systemd unit file:
```
cp /snap/pyefis/current/extras/pyefis.service ~/.config/systemd/user/
```

If you want to change the config file used edit the file you just copied and make that change.<br>

Enable automatic start of pyefis
```
systemctl --user enable pyefis.service
```

Start pyefis:
```
systemctl --user start pyefis.service
```

### Get data needed for Virtual VFR
The virtual VFR feature uses FAA data to display runways and glide slop indicators in the atitude indicator.

#### Create directory for the CIFP data
```
mkdir ~/makerplane/pyefis/CIFP/
cd ~/makerplane/pyefis/CIFP/
```

#### Download the CIFP Data
Visit https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/cifp/download/ and copy the link to the latest data.

Download the latest data using the link you copied and unzip it
```
wget https://aeronav.faa.gov/Upload_313-d/cifp/CIFP_231228.zip
unzip CIFP_231228.zip
```

Create the index:
```
pyefis.makecifpindex FAACIFP18
```

When updating in the future just delete the CIFP directory and start over at the beginning of this section


### Important information:
NOTE: Upon starting a folder named makerplane will be created in your home folder and default configs copied into that folder.<br>
It will not overwrite any file that currently exists so your customizations are safe. If you would like to get updated default configs you could delete the old configs and then start pyefis and fixgateway.<br>

Directories you need to know:
pyefis configs: ~/makerplane/pyefis/config
fixgateway configs: ~/makerplane/fixgw/config
flight data recorder logs: ~/makerplane/pyefis/fdr

Commands:
* stop fixgateway: `systemctl --user stop fixgateway.service` 
* start fixgateway: `systemctl --user start fixgateway.service`
* stop pyefis: `systemctl --user stop pyefis.service`
* start pyefis: `systemctl --user start pyefis.service`
* While stopped you can run them manually to see real time debug output:
* pyefis: `pyefis --config-file=$HOME/makerplane/pyefis/config/main.yaml --debug`
* fixgateway: `fixgateway.server --config-file=$HOME/makerplane/fixgw/config/default.yaml --debug`
* fixgateway client: `fixgatewa.client`
* CIFP index builder: `pyefis.makecifpindex`

Installing pyefis and fixgateway updates:
```
systemctl --user stop fixgateway.service
systemctl --user stop pyefis.service
snap refresh
systemctl --user start fixgateway.service
systemctl --user start pyefis.service
```

### Setup Android
If you want to use the Android feature you can find directions to setup Android [Here](ANDROID.md)

