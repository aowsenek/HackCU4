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
        if dist - prev > threshold:
            callback()
        prev = dist

def callback(client):
    def f():
        t = datetime.datetime(1996, 1, 2).now().isoformat()
        lat = 40.009700
        lon = -105.241974
        
        client.publish("pothole", """{
                "latitude": %f,
                "longitude": %f,
                "time": "%s"
            }""" % (lat, lon, time))

if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("192.168.43.140", 1883, 60)

    detect_pothole()

    client.disconnect()
