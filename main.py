#! python

import paho.mqtt.client as mqtt

if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    client.publish("this/is/a/topic", "{\"this\": \"is the message data\"}")

    client.disconnect()

