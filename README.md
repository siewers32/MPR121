# Capakang

## Capacative sensor mpr121 on raspberry pi
* MPR121
* MIDI
* Midi over Wifi

## Install
* Raspberry Pi OS Lite (64-bit)
* Enable I2C on raspberry pi
* Enable ssh on raspberry pi
* Creeer ssh-key voor github
* sudo apt update
* sudo apt upgrade
* sudo apt install git
* sudo apt install python3 python3-dev
* sudo apt install libavahi-client3 (na deze actie was rtpmidid al actief!)
* Anders....


## Midi
* Installeer rtpmidid (wget https://github.com/davidmoreno/rtpmidid/releases/download/v24.12/rtpmidid_24.12.2_arm64.deb)

```shell
dpkg -i rtpmidid.deb
apt -f install
```

* python -m venv venv
* source venv/bin/activate
* python -m pip install python-rtmidi
* Probeer onderstaande code (kies machine waarnaar midi-message verzonden moet worden)

```python

import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

# Geet user input to select a port
for i, port in enumerate(available_ports):
    print(f"{i}: {port}")
input_port = input("Select a port number to open (or press Enter for virtual port): ")
if input_port.isdigit() and int(input_port) < len(available_ports):
    midiout.open_port(int(input_port))
elif input_port.strip() == "":
    midiout.open_virtual_port("My virtual output")
    

with midiout:
    note_on = [0x90, 105, 112] # channel 1, middle C, velocity 112
    note_off = [0x80, 105, 0]
    midiout.send_message(note_on)
    time.sleep(0.5)
    midiout.send_message(note_off)
    time.sleep(0.1)

del midiout

```

## Sensor
* Installeer python -m pip install RPi.GPIO
* Installeer adafruit_blinka (python -m pip install adafruit_blinka)
* Installeer python -m pip install adafruit-circuitpython-mpr121

```python
import time
import board
import busio

# Import MPR121 module.
import adafruit_mpr121

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)

# Note you can optionally change the address of the device:
# mpr121 = adafruit_mpr121.MPR121(i2c, address=0x91)

# Loop forever testing each input and printing when they're touched.
while True:
    # Loop through all 12 inputs (0-11).
    for i in range(12):
        # Call is_touched and pass it then number of the input.  If it's touched
        # it will return True, otherwise it will return False.
        if mpr121[i].value:
            print(f"Input {i} touched!")
    time.sleep(0.25)  # Small delay to keep from spamming output messages.

```

## Links
* [checkcheckonetwo.com](https://discourse.checkcheckonetwo.com/t/how-to-install-rtpmidi-on-raspberrypi-or-other-linux-sbc/4111)
* [Python-rtpmidi](https://github.com/SpotlightKid/python-rtmidi/tree/master)
* [David Moreno RTPMidi](https://github.com/davidmoreno/rtpmidid)
* [Adafruit MPR121](https://learn.adafruit.com/adafruit-mpr121-12-key-capacitive-touch-sensor-breakout-tutorial/python-circuitpython)