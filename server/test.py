#! python3

import paho.mqtt.client as mqtt


def on_connect(client, user_data, flags, rc):
    print(client, user_data, flags, rc)

def on_message(client, user_data, msg):
    print(client, user_data, msg)

if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("127.0.0.1",1883,60)
    
    client.on_connect = on_connect
    client.on_message = on_message

    client.publish("test", "{\"location\": \"Hello World\"}");
    
    client.disconnect()
