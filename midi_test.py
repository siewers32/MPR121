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