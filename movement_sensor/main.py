import RPi.GPIO as GPIO
import time
import os
import json
from datetime import datetime

# Function to load configuration
def load_config(config_path='config.json', default_config=None):
    if default_config is None:
        default_config = {
            'DELAY_TIME': 60,
            'PIR_PIN': 17,
            'RESTRICTED_START_TIME': "07:15",
            'RESTRICTED_END_TIME': "15:15"
        }
    
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print("Configuration file not found. Using default values.")
        config = default_config

    return config

# Function to toggle monitor
def toggle_monitor(state):
    action = '--on' if state else '--off'
    os.system(f"wlr-randr --output HDMI-A-1 {action}")
    state_str = 'on' if state else 'off'
    print(f"Monitor turned {state_str}.")

# Function to check if current time is in restricted range
def is_in_time_range(start_time, end_time):
    current_time = datetime.now().time()
    return start_time <= current_time <= end_time

# Main function
def main():
    config = load_config()
    
    PIR_PIN = config.get('PIR_PIN', 17)
    DELAY_TIME = config.get('DELAY_TIME', 60)
    restricted_start_time = datetime.strptime(config.get('RESTRICTED_START_TIME', "07:15"), "%H:%M").time()
    restricted_end_time = datetime.strptime(config.get('RESTRICTED_END_TIME', "15:15"), "%H:%M").time()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)
    
    monitor_on = False
    last_motion_time = 0

    # Ensure the monitor is off at the start
    toggle_monitor(False)
    print("Monitor is off by default. Waiting for motion...")

    try:
        while True:
            current_time = datetime.now().time()

            # Turn off the monitor if within restricted time or past the restricted end time
            if is_in_time_range(restricted_start_time, restricted_end_time) or current_time > restricted_end_time:
                if monitor_on:
                    print("Within restricted time or past end time. Turning monitor off.")
                    toggle_monitor(False)
                    monitor_on = False
            else:
                if GPIO.input(PIR_PIN):
                    last_motion_time = time.time()
                    if not monitor_on:
                        print("Motion detected! Turning monitor on.")
                        toggle_monitor(True)
                        monitor_on = True
                elif monitor_on and (time.time() - last_motion_time > DELAY_TIME):
                    print(f"No motion for {DELAY_TIME} seconds. Turning monitor off.")
                    toggle_monitor(False)
                    monitor_on = False

            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
