from threading import Event
import time
import requests
import paho.mqtt.client as mqtt
import json

# ==== BENUTZER-EINSTELLUNGEN =====================

shelly_devices = [
    {"ip": "192.168.178.53", "topic": "ShellyVerbrauch1/python"},
    {"ip": "192.168.178.54", "topic": "ShellyVerbrauch2/python"},
    {"ip": "192.168.178.64", "topic": "ShellyVerbrauch3/python"},
    {"ip": "192.168.178.65", "topic": "ShellyVerbrauch4/python"},
    {"ip": "192.168.178.59", "topic": "ShellyVerbrauch5/python"}
]

# MQTT-Einstellungen
MQTT_BROKER = "192.168.178.63"
MQTT_CLIENT_ID = "Shelly_Plus_Client"
FREQUENCY = 1.0
INTERVAL_SECONDS = 1.0 / FREQUENCY

mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID)
measurement_active = Event()
Task_mode = None  # Globale Variable für den Task-Modus

def on_message(client, userdata, msg):
    global task_list
    global message_count
    message = msg.payload.decode()
    topic = msg.topic

    print(f"Message received on {msg.topic}: {message}")

    # count messages on the results topic
    if topic == MQTT_Result_Topic:
        message_count += 1
        if message_count == task_count and task_count > 0:
            log_event(f"All tasks have been processed: done_tasks = {message_count}, init_tasks = {task_count}")
            client.publish("start_stop/taskWorker", 0, qos=1)  # stop worker
            client.publish("start_stop/shelly", "stop", qos=1)  # STOP Shelly Messung
            print("# Nicole: Shelly Messung gestoppt")

    # check for status messages
    if topic.startswith("status/"):
        client_name = topic.split("/")[1]
        if "Disconnected" in message:
            connected_clients.discard(client_name)
        elif "Connected" in message:
            connected_clients.add(client_name)
    elif topic.startswith("ping/response/"):
        client_name = topic.split("/")[-1]
        connected_clients.add(client_name)
    elif topic.startswith("task_generator"):
        print("Task generator triggered. Loading tasks...")
        load_tasks_from_file()

    match = re.search(r"My name is (\w+)", message)
    if match:
        connected_pc = match.group(1)
        connected_clients.add(connected_pc)

if __name__ == '__main__':
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username=MQTT_Username, password=MQTT_Password)
    client.will_set(f"status/{client_id}", "Disconnected", qos=1, retain=True)

    MQTT_Broker = get_broker_ip_via_file()
    Broker_Port = 1883

    try:
        client.connect(MQTT_Broker, Broker_Port)

        # START Shelly Messung vor Aufgabenverteilung
        client.publish("start_stop/shelly", "start", qos=1)
        print("# Nicole: Shelly Messung gestartet")

        # Zusatzinfo (task_mode) wurde bereits oben versendet

        ping_thread = threading.Thread(target=send_ping, args=(client,))
        monitor_thread = threading.Thread(target=monitor_clients)
        task_thread = threading.Thread(target=distribute_tasks, args=(client,))

        ping_thread.start()
        monitor_thread.start()
        task_thread.start()

        client.loop_forever()
    except Exception as e:
        print(f"Error connecting to MQTT Broker: {e}")