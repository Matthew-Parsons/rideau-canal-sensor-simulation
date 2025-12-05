import time
import random
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRINGS = ["Your IoT Hub device connection string here", "connection2", "connection3"]

def get_telemetry():
    return {
        "surface-temperature": random.uniform(-20.0, 5.0),
        "ice-thickness": random.uniform(15.0, 70.0),
        "snow-accumulation": random.uniform(0.0, 30.0),
        "external-temperature": random.uniform(-20.0, 5.0)
    }

def main():
    clients = [IoTHubDeviceClient.create_from_connection_string(cs) for cs in CONNECTION_STRINGS]

    print("Sending telemetry from 3 devices to IoT Hub...")
    try:
        while True:
            for i, client in enumerate(clients, start=1):
                telemetry = get_telemetry()
                message = Message(str(telemetry))
                client.send_message(message)
                print(f"Sent message: {message}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped sending messages.")
    finally:
        for client in clients:
            client.disconnect()

if __name__ == "__main__":
    main()