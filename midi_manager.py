import time
import rtmidi

class MidiManager:
    def __init__(self, midiout):
        self.midiout = midiout
        self.available_ports = midiout.get_ports()
        self.port = 0
        self.notes = [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91]  # Example MIDI notes
        

    def show_ports(self):
        """Display available MIDI ports."""
        for i, port in enumerate(self.available_ports):
            print(f"{i}: {port}")
        selection = input("Select a port number to open: ")
        if selection.isdigit() and int(selection) < len(self.available_ports):
            self.port = int(selection)
            self.midiout.open_port(self.port)
        elif selection.strip() == "":
            self.port = 0
            self.midiout.open_virtual_port("My virtual output")

    def send_note(self, note, velocity=112):
        """Send a MIDI note on message."""
        if self.midiout:
            print(f"Sent Note On: {note} with velocity {velocity}")
            note_on = [0x90, note, velocity]  # channel 1, middle C, velocity 112
            note_off = [0x80, note, 0]
            self.midiout.send_message(note_on)
            time.sleep(0.5)
            self.midiout.send_message(note_off)
            time.sleep(0.1)

