import requests
import influxdb_client
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load configuration from config.json
config_path = os.path.join(script_dir, 'config.json')
with open(config_path) as config_file:
    config = json.load(config_file)

temperature_ip_addresses = config["temperature_ip_addresses"]
power_ip_addresses = config["power_ip_addresses"]
air_quality_ip_addresses = config["air_quality_ip_addresses"]
token = config["influxdb_token"]

org = "Ford"
url = "http://mm2.local:8086"
bucket = "iobroker"
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

def print_error(message):
    print(f"\033[91m[Error] {message}\033[0m")

def print_info(message):
    print(f"[Info] {message}")

def get_temperature(ip):
    url = f"http://{ip}/status"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        temperature = data['thermostats'][0]['tmp']['value']
        return temperature
    except requests.exceptions.RequestException as e:
        print_error(f"Error fetching temperature data from {ip}")
        return None
    except (KeyError, IndexError) as e:
        print_error(f"Error parsing temperature data from {ip}")
        return None

def get_power_data(ip):
    url = f"http://{ip}/status"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        power = data['meters'][0]['power']
        return power
    except requests.exceptions.RequestException as e:
        print_error(f"Error fetching power data from {ip}: {e}")
        return None
    except (KeyError, IndexError) as e:
        print_error(f"Error parsing power data from {ip}: {e}")
        return None

def get_air_data(ip):
    url = f"http://{ip}/air-data/latest"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print_error(f"Error fetching air data from {ip}: {e}")
        return None
    except (KeyError, IndexError) as e:
        print_error(f"Error parsing air data from {ip}: {e}")
        return None

def store_temperature_data(ip, temperature):
    try:
        point = (
            Point("temperature")
            .tag("device", ip)
            .field("value", temperature)
        )
        write_api.write(bucket=bucket, org=org, record=point)
        print_info(f"Temperature data from {ip} written to InfluxDB.")
    except Exception as e:
        print_error(f"Error writing temperature data to InfluxDB: {e}")

def store_power_data(ip, power):
    try:
        point = (
            Point("power")
            .tag("device", ip)
            .field("value", power)
        )
        write_api.write(bucket=bucket, org=org, record=point)
        print_info(f"Power data from {ip} written to InfluxDB.")
    except Exception as e:
        print_error(f"Error writing power data to InfluxDB: {e}")

def store_air_data(ip, air_data):
    try:
        point = (
            Point("air_quality")
            .tag("device", ip)
            .field("score", air_data["score"])
            .field("dew_point", air_data["dew_point"])
            .field("temp", air_data["temp"])
            .field("humid", air_data["humid"])
            .field("abs_humid", air_data["abs_humid"])
            .field("co2", air_data["co2"])
            .field("co2_est", air_data["co2_est"])
            .field("co2_est_baseline", air_data["co2_est_baseline"])
            .field("voc", air_data["voc"])
            .field("voc_baseline", air_data["voc_baseline"])
            .field("voc_h2_raw", air_data["voc_h2_raw"])
            .field("voc_ethanol_raw", air_data["voc_ethanol_raw"])
            .field("pm25", air_data["pm25"])
            .field("pm10_est", air_data["pm10_est"])
        )
        write_api.write(bucket=bucket, org=org, record=point)
        print_info(f"Air quality data from {ip} written to InfluxDB.")
    except Exception as e:
        print_error(f"Error writing air quality data to InfluxDB: {e}")

# Retrieve and store temperature data
for ip in temperature_ip_addresses:
    temp = get_temperature(ip)
    if temp is not None:
        print_info(f"Current temperature at {ip}: {temp}°C")
        store_temperature_data(ip, temp)
    else:
        print_error(f"Could not retrieve temperature data from {ip}")

# Retrieve and store power data
for ip in power_ip_addresses:
    power = get_power_data(ip)
    if power is not None:
        print_info(f"Current power at {ip}: {power}W")
        store_power_data(ip, power)
    else:
        print_error(f"Could not retrieve power data from {ip}")

# Retrieve and store air quality data
for ip in air_quality_ip_addresses:
    air_data = get_air_data(ip)
    if air_data is not None:
        print_info(f"Current air data at {ip}: {air_data}")
        store_air_data(ip, air_data)
    else:
        print_error(f"Could not retrieve air data from {ip}")