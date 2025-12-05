import time
import random
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRINGS = ["HostName=rideau-canal-iot.azure-devices.net;DeviceId=NAC;SharedAccessKey=pCh80tlnb2WzaDBLx+HJvC+IdSG9qs7ArlxoLrrzMHI=", 
                      "HostName=rideau-canal-iot.azure-devices.net;DeviceId=Dow's-Lake;SharedAccessKey=Zo3T/1c8or7dJTqkHxX+aPRlZGlhZnKDjqoIOmHP+KM=", 
                      "HostName=rideau-canal-iot.azure-devices.net;DeviceId=Fifth-Avenue;SharedAccessKey=wgemEh+UQ6TcVJq/A5e/25kN0ZrKfdDfvYc6HjS/1n8="]

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