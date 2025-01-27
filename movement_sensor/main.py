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
            'START_TIME': "07:15",
            'END_TIME': "15:15"
        }
    
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print("Configuration file not found. Using default values.")
        config = default_config

    print(f"Configuration loaded: {config}")
    return config

# Function to toggle monitor
def toggle_monitor(state):
    action = '--on' if state else '--off'
    os.system(f"wlr-randr --output HDMI-A-1 {action}")
    state_str = 'on' if state else 'off'
    print(f"Monitor turned {state_str}.")

# Function to check if current time is within the allowed range
def is_within_allowed_time(start_time, end_time):
    current_time = datetime.now().time()
    if start_time <= end_time:
        return start_time <= current_time < end_time
    else:  # Over midnight
        return current_time >= start_time or current_time < end_time

# Main function
def main():
    config = load_config()
    
    PIR_PIN = config.get('PIR_PIN', 17)
    DELAY_TIME = config.get('DELAY_TIME', 60)
    start_time = datetime.strptime(config.get('START_TIME', "07:15"), "%H:%M").time()
    end_time = datetime.strptime(config.get('END_TIME', "15:15"), "%H:%M").time()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)
    
    monitor_on = True  # Assume the monitor is on initially
    last_motion_time = 0

    # Check initial time and set monitor state accordingly
    if is_within_allowed_time(start_time, end_time):
        toggle_monitor(False)
        monitor_on = False
        print("Monitor is off by default during allowed time. Waiting for motion...")
    else:
        toggle_monitor(True)
        monitor_on = True
        print("Monitor remains on outside of allowed time.")

    try:
        while True:
            if is_within_allowed_time(start_time, end_time):
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
            else:
                if not monitor_on:
                    print("Outside of allowed time. Turning monitor on.")
                    toggle_monitor(True)
                    monitor_on = True
                # Do not control the monitor outside of allowed time
                # Monitor remains on
                
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
