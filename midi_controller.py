import time
import board
import busio
import adafruit_mpr121

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)

def send_midi_message(note, velocity=127):
    """Send a MIDI message."""
    # This function should be implemented to send MIDI messages.
    # For example, using a MIDI library or protocol.
    print(f"Sending MIDI message: Note {note}, Velocity {velocity}")

while True:
    # Loop through all 12 inputs (0-11).
    for i in range(12):
        # Call is_touched and pass it then number of the input.  If it's touched
        # it will return True, otherwise it will return False.
        if mpr121[i].value:
            send_midi_message(note=i + 60)
    time.sleep(0.25)  # Small delay to keep from spamming output messages.
