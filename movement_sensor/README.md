# AzubiReflektorScripts
Scripts für MagicMirror2

# Raspberry Pi Motion-Activated Monitor Control

This project uses a Raspberry Pi and a PIR sensor to automatically turn a monitor on or off based on detected motion.

## Features

- Monitors motion using a PIR sensor
- Automatically turns the monitor on when motion is detected
- Turns the monitor off after a specified delay if no motion is detected
- Configurable delay and PIR sensor pin via a JSON file

## Requirements

- Raspberry Pi
- PIR Motion Sensor
- HDMI Monitor
- Python 3
- `RPi.GPIO` library
- `wlr-randr` command-line tool

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/davinci05/AzubiReflektorScripts.git
    cd AzubiReflektorScripts
    ```

2. **Install Dependencies**

Make sure you have Python 3 and the required libraries installed:

    ```bash
    sudo apt-get update
    sudo apt-get install python3-pip
    pip3 install RPi.GPIO
    ```

3. **Install wlr-randr**

Follow the instructions here to install wlr-randr.

Configuration
Edit the config.json file to set your desired delay time and PIR sensor GPIO pin:

    ```json

    {
        "DELAY_TIME": 60,
        "PIR_PIN": 17
    }```

DELAY_TIME: Time in seconds before the monitor turns off after no motion is detected.
PIR_PIN: GPIO pin number where the PIR sensor is connected.
Usage
Run the script using Python 3:


    ```bash
    python3 main.py
    ```
