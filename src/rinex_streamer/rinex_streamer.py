import os
import time
import paho.mqtt.client as mqtt
from gnss_tec import rnx

RINEX_DIRECTORY = "/app/data/rinex_files/ANTC00CHL"  # Директория внутри контейнера

def process_rinex(file_path):
    with open(file_path) as obs_file:
        reader = rnx(obs_file)
        for tec in reader:
            print(f'{tec.timestamp} {tec.satellite}: {tec.phase_tec} {tec.p_range_tec}')

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("rinex_files")

def on_message(client, userdata, msg):
    file_name = msg.payload.decode()
    file_path = os.path.join(RINEX_DIRECTORY, file_name)
    print(f"Processing file: {file_path}")
    if os.path.isfile(file_path):
        process_rinex(file_path)
    else:
        print(f"File not found: {file_path}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt_broker", 1883, 60)
client.loop_start()

while True:
    time.sleep(1)
