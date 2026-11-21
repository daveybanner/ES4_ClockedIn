import serial
import json
import threading
import time

SERIAL_PORT = 'COM9'  # Update to your port (e.g., '/dev/ttyUSB0' on Linux/Mac)
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Wait briefly for serial connection to stabilize

def read_from_esp32():
    """Background thread to continuously read incoming data."""
    while ser.is_open:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(f"\n[ESP32]: {line}\nCommand (on/off/quit): ", end="")
        except Exception:
            break

# Start the background listener thread
listener = threading.Thread(target=read_from_esp32, daemon=True)
listener.start()

print("Connected! Type 'on' or 'off' to toggle the ESP32 LED, or 'quit' to exit.")

try:
    while True:
        user_input = input("Command (on/off/quit): ").strip().lower()
        
        if user_input == 'quit':
            break
        elif user_input in ['on', 'off']:
            payload = {
                "action": "led",
                "value": True if user_input == 'on' else False
            }
            # Convert to JSON string, add newline '\n', and encode to bytes
            message = json.dumps(payload) + '\n'
            ser.write(message.encode('utf-8'))
        else:
            print("Invalid command. Use 'on', 'off', or 'quit'.")

except KeyboardInterrupt:
    pass
finally:
    ser.close()
    print("\nSerial connection closed.")
