import paho.mqtt.client as mqtt
import json
import os

MQTT_BROKER = "mqtt_broker"
MQTT_PORT = 1883
MQTT_TOPIC = "satellite/data"

def publish_data(file_path):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    with open(file_path, 'r') as f:
        data = f.read()
        client.publish(MQTT_TOPIC, data)
        print(f"Отправлено сообщение из {file_path} в топик {MQTT_TOPIC}")

    client.disconnect()

if __name__ == "__main__":
    file_path = "/path/to/rinex/file.rnx"  # Укажите путь к файлу RINEX
    publish_data(file_path)

