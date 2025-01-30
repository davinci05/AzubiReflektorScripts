import RPi.GPIO as GPIO
import time
import os

# Configuration
PIR_PIN = 17          # GPIO pin for PIR sensor
DELAY_TIME = 60       # Time in seconds before turning off the monitor
INITIAL_DELAY = 30    # Initial delay for PIR sensor stabilization

def turn_monitor_on():
    print("Turning monitor on.")
    # Use xset to turn on the monitor
    os.system("xset dpms force on")

def turn_monitor_off():
    print("Turning monitor off.")
    # Use xset to turn off the monitor
    os.system("xset dpms force off")

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)

    print("Initializing PIR sensor...")
    time.sleep(INITIAL_DELAY)
    print("PIR sensor ready.")

    last_motion_time = 0
    monitor_on = False  # Assume monitor is off initially

    try:
        while True:
            motion_detected = GPIO.input(PIR_PIN)

            if motion_detected:
                last_motion_time = time.time()
                if not monitor_on:
                    print("Motion detected! Turning monitor on.")
                    turn_monitor_on()
                    monitor_on = True
            else:
                if monitor_on and (time.time() - last_motion_time > DELAY_TIME):
                    print(f"No motion for {DELAY_TIME} seconds. Turning monitor off.")
                    turn_monitor_off()
                    monitor_on = False

            time.sleep(1)  # Update every second

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
        turn_monitor_off()  # Ensure monitor is off when exiting

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
