import RPi.GPIO as GPIO
import time
import os

# GPIO-Nummer für den PIR-Sensor
PIR_PIN = 17  # OUT-Pin des PIR-Sensors

# GPIO initialisieren
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)  # PIR-Sensor als Eingang

# Variablen zur Steuerung des Timers
monitor_on = False
last_motion_time = 0  # Zeitpunkt der letzten Bewegung
DELAY_TIME = 10  # Wartezeit in Sekunden, bevor der Monitor ausgeht

print("Warte auf Bewegung...")

try:
    while 1:
        if GPIO.input(PIR_PIN):  # Bewegung erkannt
            last_motion_time = time.time()  # Aktuelle Zeit speichern
            if not monitor_on:  # Falls Monitor aus ist, einschalten
                print("Bewegung erkannt! Monitor wird eingeschaltet.")
                os.system("wlr-randr --output HDMI-A-1 --on")
                monitor_on = True
        
        # Prüfe, ob die letzte Bewegung länger als DELAY_TIME her ist
        elif monitor_on and (time.time() - last_motion_time > DELAY_TIME):
            print("Keine Bewegung für 10 Sekunden. Monitor wird ausgeschaltet.")
            os.system("wlr-randr --output HDMI-A-1 --off")
            monitor_on = False
        
        time.sleep(1)  # Kürzere Abfrage, um schneller zu reagieren

except KeyboardInterrupt:
    print("Beende das Programm.")
    GPIO.cleanup()  # GPIO-Pins aufräumen
