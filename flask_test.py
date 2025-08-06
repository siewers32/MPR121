from flask import Flask, render_template
from flask_socketio import SocketIO
from waitress import serve
import time
import rtmidi
from midi_manager import MidiManager
from sensor_manager import SensorManager
import time
import board
import busio
import adafruit_mpr121
import subprocess
import sys
import os
import threading

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


app = Flask(__name__) 
socketio = SocketIO(app) 

FILE_PATH = "test.txt"

# Laatst bekende wijzigingstijd van het bestand
last_modified = 0

def monitor_file():
    """Een achtergrond-thread die het bestand controleert op wijzigingen."""
    global last_modified
    while True:
        if os.path.exists(FILE_PATH):
            current_modified = os.path.getmtime(FILE_PATH)
            
            # Als de wijzigingstijd is veranderd, lees het bestand en verstuur de data
            if current_modified > last_modified:
                last_modified = current_modified
                print("Bestand gewijzigd! Nieuwe data versturen...")
                
                with open(FILE_PATH, 'r') as f:
                    data = f.read()
                
                # 'data_updated' is een custom event-naam
                socketio.emit('data_updated', {'file_data': data})
        
        # Wacht 1 seconde voordat het opnieuw wordt gecontroleerd (dit is nog steeds polling, maar dan op de server in een aparte thread)
        time.sleep(1)

@app.route("/")
def index():
    """Render de hoofdpagina."""
    return render_template('index.html')

# def handle_connect():
#     """Handler voor nieuwe clientverbindingen."""
#     print("Nieuwe client verbonden!")
#     if os.path.exists(FILE_PATH):
#         with open(FILE_PATH, 'r') as f:
#             data = f.read()
#         socketio.emit('data_updated', {'file_data': data})

@app.route("/home")  
# Definieer een route middels deze annotatie
def home():
    return render_template('select_port.html', midi_manager=midi_manager)

def select_port():
    """Handle port selection and open the selected MIDI port."""
    if 'port_number' in request.form:
        port_number = request.form['port_number']
        if port_number.isdigit() and int(port_number) < len(midi_manager.available_ports):
            midi_manager.port = int(port_number)
            midiout.open_port(midi_manager.port)
        else:
            midi_manager.port = 0
            midiout.open_virtual_port("My virtual output")
    return "Port selected successfully!" 

@app.route("/test_port", methods=["POST"])
def test_port():
    venv_python = sys.executable
    subprocess.Popen([venv_python, 'main.py'])
    return render_template('record.html')

if __name__ == "__main__":
    # Automatisch herstarten bij wijzigingen in de code
    # app.run(debug=True, use_reloader=True)
    
    # Niet herstarten na wijzigingen in de code
    # app.run(debug=True, use_reloader=False)
    
    # Produtctieserver gebruiken (waitress)
    # serve(app, host='0.0.0.0', port=8000)
    
    thread = threading.Thread(target=monitor_file)
    thread.daemon = True # Zorgt ervoor dat de thread stopt als de hoofdthread stopt
    thread.start()
    
    socketio.run(app, debug=True)

    # Start de server