#! python3

import json

import paho.mqtt.client as mqtt

import twitter

import keys

api = None

def init_twitter():
    global api
    
    api = twitter.Api(
        consumer_key=keys.consumer_key,
        consumer_secret=keys.consumer_secret,
        access_token_key=keys.access_token_key,
        access_token_secret=keys.access_token_secret
    )
    
    return api

def on_connect(client, user_data, flags, rc):
    print(client, user_data, flags, rc)

def on_message(client, user_data, msg):
    topic = msg.topic
    
    try:
        payload = msg.payload.decode("utf-8")
    except UnicodeDecodeError:
        print("Failed to interperet the following hex as a UTF-8 string:\n"
             f"\t0x{msg.payload.hex()}")
        return
        
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print(f"Failed to decode {payload} as JSON.")
        return
    
    location = data.get("location", "")
    
    if location:
        try:
            status = api.PostUpdate(location)
        except UnicodeDecodeError:
            print("Tweet location included invalid characters.")
            return
        
        print(f"Tweet posted with {status}.")
    else:
        print("No location found in the message data.")

if __name__ == "__main__":
    init_twitter()
    
    client = mqtt.Client()
    client.connect("127.0.0.1",1883,60)

    client.on_connect = on_connect
    client.on_message = on_message

    client.subscribe("test", 0)

    client.loop_forever()
