#! python3

import json
import sqlite3
import twitter
import keys

import paho.mqtt.client as mqtt

api = None
db = None

def init_twitter():
    global api
    
    api = twitter.Api(
        consumer_key=keys.consumer_key,
        consumer_secret=keys.consumer_secret,
        access_token_key=keys.access_token_key,
        access_token_secret=keys.access_token_secret
    )
    
    return api

def init_db():
    global db

    db = sqlite3.connect('potholes.db')

def add_pothole(lat, lon):
    global db

    if db is None:
        print("Database is none!")
        return
    THRESHOLD = 0.5;
    c = db.cursor()
    # I can't find SQLite's power function -Alex
    c.execute("SELECT * FROM holes WHERE ((lat-?)+(lon-?))*((lat-?)+(lon-?)) < ?*?", (lat, lon, lat, lon, THRESHOLD, THRESHOLD))
    closest = c.fetchone()
    if closest is None:
        c.execute("INSERT INTO holes (LAT, LON, COUNT) VALUES (?, ?, ?)", (lat, lon, 1))
    else:
        i, _, _, count = closest
        c.execute("UPDATE holes SET count = ? WHERE id = ?", (count + 1, i))
    db.commit()

def close_db():
    global db

    db.close()

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
    
    location = data.get("tweet", "")
    
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
    init_db()
    init_twitter()
    
    client = mqtt.Client()
    client.connect("127.0.0.1",1883,60)

    client.on_connect = on_connect
    client.on_message = on_message

    client.subscribe("pothole", 0)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        pass

    close_db()
