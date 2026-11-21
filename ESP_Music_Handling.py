from machine import Pin, ADC
import time
import random
import json
import sys
import select

# Pin declarations
diff_in = {Pin(3, Pin.IN), Pin(4, Pin.IN)}
FPGA_start = Pin(5, Pin.IN)
beat_strt_out = Pin(6, Pin.OUT)

# Global Variables
MAX_SONGS = 4
hard_songs = {}
medium_songs = {}
easy_songs = {}

while True:
    # Wait for FPGA to trigger start condition
    while True:
        if FPGA_start:
            break
    
    # Randomly select song from selected difficulty
    song_select = random.randint(0, 4)
    selected_song = ""
    if diff[1]:
        selected_song = hard_songs[song_select]
    elif diff[0]:
        selected_song = medium_songs[song_select]
    else:
        selected_song = easy_songs[song_select]
       
    # Give song data to laptop
    print(json.dumps({"song": selected_song}))

    # Start listening for Laptop input
    poll_obj = select.poll()
    poll_obj.register(sys.stdin, select.POLLIN)

    while True:
        if poll_obj.poll(0):
            line = sys.stdin.readline().strip()
            if line:
                try:
                    # Get input from laptop 
                    cmd = json.loads(line)
                    if cmd.get("action") == "start":
                        state = 1 if cmd.get("value") else 0
                        beat_strt_out.value(state)
                        print(json.dumps({"ack": "beat_started", "state": state}))
                        break
                except ValueError:
                    print(json.dumps({"error": "invalid_json", "raw": line}))
                
