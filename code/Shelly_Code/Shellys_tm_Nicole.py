from threading import Event
import time
import requests
import paho.mqtt.client as mqtt
import json

# ==== BENUTZER-EINSTELLUNGEN =====================

shelly_devices = [
    {"ip": "192.168.178.53", "topic": "Shelly1_ThinkPad"},
    {"ip": "192.168.178.54", "topic": "Shelly2_HP"},
    {"ip": "192.168.178.79", "topic": "Shelly3_Pi5_16GB"},
    {"ip": "192.168.178.80", "topic": "Shelly4_Pi5_8GB"},
    {"ip": "192.168.178.59", "topic": "Shelly5_Pi4_8GB"}
]
global MQTT_BROKER
global MQTT_CLIENT_ID
global FREQUENCY   

# MQTT-Einstellungen
MQTT_BROKER = "192.168.178.63" # TODO: Broker nicht hard coden
MQTT_CLIENT_ID = "Shelly_Plus_Client"
FREQUENCY = 1.02 #??
INTERVAL_SECONDS = 1.0 / FREQUENCY
task_mode  = ""
total_task_count = ""
num_conn_clients = ""
tasks_per_client = ""
iteration = ""

measurement_active = Event()

def on_connect(client, userdata, flags, rc):
    print(f"Verbunden mit MQTT-Broker: {MQTT_BROKER}")
    client.subscribe("start_stop/taskWorker") #random+efficient tm
    client.subscribe("start_stop/zusatzinfo") #tasktypes tm
    client.subscribe("infos/taskcount")
    client.subscribe("infos/clientcount") #random+efficient done
    client.subscribe("infos/task_per_client") #??nicht notwendig
    client.subscribe("infos/iteration") #random+efficient done
    client.subscribe("infos/taskmode") 

def on_message(client, userdata, msg):
    global task_mode
    global num_conn_clients
    global total_task_count
    global tasks_per_client
    global iteration

    topic = msg.topic
    message = msg.payload.decode()

    if topic == "start_stop/taskWorker":
        if message == "1":
            print("Messung global gestartet.")
            measurement_active.set()
        elif message == "0":
            print("Messung global gestoppt.")
            measurement_active.clear()
    elif topic == "infos/taskmode":
        task_mode = message
        print(f"Zusatzinfo empfangen: {task_mode}")
    elif topic == "infos/taskcount":
        total_task_count = message
        print(f"Task Count empfangen: {total_task_count}")
    elif topic == "infos/clientcount":
        num_conn_clients = message
        print(f"Num conn clients empfangen: {num_conn_clients}")
    elif topic == "infos/task_per_client":
        tasks_per_client = message
        print(f"Tasks per Client empfangen: {tasks_per_client}")
    elif topic == "infos/iteration":
        iteration = message
        print(f"Iteration empfangen: {iteration}")

if __name__ == '__main__':
    mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    mqtt_client.on_message = on_message
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(MQTT_BROKER)
    print(f"Verbunden mit MQTT-Broker: {MQTT_BROKER}")
    mqtt_client.loop_start()

    try:
        print("Warte auf Startsignal...")
        while True:
            if measurement_active.is_set():
                start_time = time.time()
                next_call = start_time

                print("Messung läuft...")

                while measurement_active.is_set():
                    current_time = time.time()

                    for device in shelly_devices:
                        url = f"http://{device['ip']}/rpc/Switch.GetStatus?id=0"
                        topic = device["topic"]

                        try:
                            response = requests.get(url, timeout=2)
                            if response.status_code == 200:
                                data = response.json()
                                data["task_mode"] = task_mode  # `task_mode` an das JSON anhängen
                                data["total_task_count"] = total_task_count  # `total_task_count` an das JSON anhängen
                                data["conn_clients"] = num_conn_clients  # `num_conn_clients` an das JSON anhängen
                                data["tasks_per_client"] = tasks_per_client  # `tasks_per_client` an das JSON anhängen
                                data["iteration"] = iteration  # `tasks_per_client` an das JSON anhängen
                                print(f"Statusdaten von {device['ip']}: {data}")
                                mqtt_client.publish(topic, json.dumps(data))
                            else:
                                print(f"Fehler bei {device['ip']}: {response.status_code}")
                        except requests.exceptions.RequestException as e:
                            print(f"Verbindungsfehler bei {device['ip']}: {e}")

                    next_call += INTERVAL_SECONDS
                    sleep_duration = max(0, next_call - time.time())
                    time.sleep(sleep_duration)

                print("Messung gestoppt. Warte auf neues Startsignal...")
            else:
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("Messung beendet.")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
