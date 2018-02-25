#! python

import paho.mqtt.client as mqtt

import mraa, time

trig_pin = mraa.Gpio(13)
echo_pin = mraa.Gpio(12)

trig_pin.dir(mraa.DIR_OUT)
echo_pin.dir(mraa.DIR_IN)

def read_dist():
    time.sleep(0.3)
    trig_pin.write(1)
    time.sleep(0.00001)
    trig_pin.write(0)

    while echo_pin.read() == 0:
        pulse_off = time.time()
    while echo_pin.read() == 1:
        pulse_on = time.time()

    d_time = pulse_on - pulse_off
    cm = d_time * 17000
    print(cm)
    return cm

def detect_pothole(callback):
    prev = read_dist()
    threshold = 20

    while True:
        dist = read_dist()
        if abs(dist - prev) > threshold:
            callback()
        prev = dist


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("192.168.43.140", 1883, 60)

    detect_pothole(lambda:
        client.publish("pothole", "{\"tweet\": \"I just ran over a pothole!\"}")
    )

    client.disconnect()

