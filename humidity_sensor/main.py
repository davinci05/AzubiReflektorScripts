import requests
import influxdb_client
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import nmap
from dotenv import load_dotenv
import os

# .env datei auslesen
load_dotenv()

# environment variablen lesen
token = os.getenv("INFLUXDB_TOKEN")
org = os.getenv("INFLUXDB_ORG")
url = os.getenv("INFLUXDB_URL")
bucket = os.getenv("INFLUXDB_BUCKET")
network_range = os.getenv("NETWORK_RANGE")

# influxdb 
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

def get_temperature(ip):
    url = f"http://{ip}/status"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        temperature = data['thermostats'][0]['tmp']['value']
        return temperature
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {ip}: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing data from {ip}: {e}")
        return None

def scan_network(network_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=network_range, arguments='-p 80 --open')
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    return [host for host, status in hosts_list if status == 'up']

def main():
    ip_addresses = scan_network(network_range)
    for ip in ip_addresses:
        temp = get_temperature(ip)
        if temp is not None:
            print(f"Current temperature at {ip}: {temp}°C")
            try:
                point = (
                    Point("temperature")
                    .tag("device", ip)
                    .field("value", temp)
                )
                write_api.write(bucket=bucket, org=org, record=point)
                print(f"Temperature data from {ip} written to InfluxDB.")
            except Exception as e:
                print(f"Error writing data to InfluxDB: {e}")
        else:
            print(f"Could not retrieve temperature from {ip}")

if __name__ == "__main__":
    main()
