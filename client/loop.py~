#!/usr/bin/python
import mraa, time


trigPin=mraa.Gpio(13)
echoPin=mraa.Gpio(12)

trigPin.dir(mraa.DIR_OUT)
echoPin.dir(mraa.DIR_IN)

print ('Starting Loop:')

while True:
  time.sleep(0.3)
  trigPin.write(1)
  time.sleep(0.00001)
  trigPin.write(0)
  while echoPin.read() == 0:   
      pulseOff = time.time()
  while echoPin.read() == 1:
      pulseOn = time.time()
  timeDifference = pulseOn - pulseOff
  centimeters = timeDifference * 17000
  print centimeters
  
#while 1:
#  trig.write(0)
#  time.sleep(.2)
#  
#  trig.write(1)
#  time.sleep(.00001)
#  trig.write(0)
#
#  duration=echo.read()
#
#  distance=duration*.034/2
#
#  print('Duration: %s' %  duration)
#  print('Distance: %s' % distance)
#







