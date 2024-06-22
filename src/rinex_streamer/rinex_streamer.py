import os
import json
import time
import paho.mqtt.client as mqtt
from gnss_tec import rnx

MQTT_BROKER = "mqtt_broker"
MQTT_PORT = 1883
MQTT_TOPIC = "satellite/data"

def process_rinex(file_path):
    with open(file_path) as obs_file:
        reader = rnx(obs_file)
        for tec in reader:
            data = {
                'timestamp': str(tec.timestamp),
                'satellite': tec.satellite,
                'phase_tec': tec.phase_tec,
                'p_range_tec': tec.p_range_tec
            }
            publish_data(data)

def publish_data(data):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, json.dumps(data))
    client.disconnect()

if __name__ == "__main__":
    file_path = "/path/to/rinex/file.rnx"  # Укажите путь к файлу RINEX
    process_rinex(file_path)

