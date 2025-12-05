import time
import random
import threading
from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv
import os

load_dotenv()

DowsLakeDevice = os.getenv("DOWS_LAKE_CONNECTION_STRING")
FifthAvenueDevice = os.getenv("FIFTH_AVENUE_CONNECTION_STRING")
NACDevice = os.getenv("NAC_CONNECTION_STRING")

def get_telemetry(location):
    return {
        "location": location,
        "surface_temperature": random.uniform(-20.0, 5.0),
        "ice_thickness": random.uniform(15.0, 70.0),
        "snow_accumulation": random.uniform(0.0, 30.0),
        "ext_Temperature": random.uniform(-20.0, 5.0)
    }

def main(location,connection_string):
    client = IoTHubDeviceClient.create_from_connection_string(connection_string)

    print("Sending telemetry to IoT Hub...")
    try:
        while True:
            telemetry = get_telemetry(location)
            message = Message(str(telemetry))
            client.send_message(message)
            print(f"Sent message: {message}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped sending messages.")
    finally:
        client.disconnect()

if __name__ == "__main__":
    device_threads = [
        threading.Thread(target=main, args=("Dow's-Lake", DowsLakeDevice)),
        threading.Thread(target=main, args=("Fifth-Avenue", FifthAvenueDevice)),
        threading.Thread(target=main, args=("NAC", NACDevice))]
    for t in device_threads:
        t.start()

    for t in device_threads:
        t.join()