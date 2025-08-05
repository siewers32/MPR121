import time
import rtmidi
from midi_manager import MidiManager
from sensor_manager import SensorManager
import time
import board
import busio
import adafruit_mpr121

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)

# Create a MIDI output instance
midiout = rtmidi.MidiOut()

# Initialize the MidiManager with the MIDI output instance
midi_manager = MidiManager(midiout)

# Initialize the sensor manager
sensor_manager = SensorManager(mpr121)

# Laat gebruikers de beschikbare MIDI-poorten zien en een keuze maken
midi_manager.show_ports()

midi_loop = True
while midi_loop:
    # Read touch inputs from the MPR121 sensor
    touch_data = sensor_manager.read_touch()
    
        
    
    # If any touch inputs are detected, send corresponding MIDI messages
    for note in touch_data:
        if note == 1:
           midi_loop = False
        else:
            # Send MIDI note for the touched sensor
            print(f"Sending MIDI note for sensor {note}") 
            midi_manager.send_note(midi_manager.notes[note])  
    time.sleep(0.25)  # Small delay to prevent spamming messages

del midiout

