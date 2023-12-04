import RPi.GPIO as GPIO
import time

# pins
garbage_trigPin = 16
garbage_echoPin = 18
recycle_trigPin = 1
recycle_echoPin = 2
compost_trigPin = 3
compost_echoPin = 4

# max distance in cm for each ultrasonic sensor
# distance cannot be lower than 50
MAX_DISTANCE_BINS = 100
bins_timeout = MAX_DISTANCE_BINS * 60

# pulse time of pin timeout
def pulseIn(pin, level, timeOut):
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if ((time.time() - t0) > timeOut * 0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if ((time.time() - t0) > timeOut * 0.000001):
            return 0;
    pulseTime = (time.time() - t0) * 1000000
    return pulseTime

# get measurement in cm for garbage
def getGarbageSonar():
    GPIO.output(garbage_trigPin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(garbage_trigPin, GPIO.LOW)
    pingTime = pulseIn(garbage_echoPin, GPIO.HIGH, bins_timeout)
    distance = pingTime * 340.0 / 2.0 / 10000.0 # distance of sound speed 340m/s
    return distance

# get measurement in cm for recycle
def getRecycleSonar():
    GPIO.output(recycle_trigPin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(recycle_trigPin, GPIO.LOW)
    pingTime = pulseIn(recycle_echoPin, GPIO.HIGH, bins_timeout)
    distance = pingTime * 340.0 / 2.0 / 10000.0 # distance of sound speed 340m/s
    return distance

# get measurement in cm for compost
def getCompostSonar():
    GPIO.output(compost_trigPin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(compost_trigPin, GPIO.LOW)
    pingTime = pulseIn(compost_echoPin, GPIO.HIGH, bins_timeout)
    distance = pingTime * 340.0 / 2.0 / 10000.0 # distance of sound speed 340m/s
    return distance

def setup():
    GPIO.setup(garbage_trigPin, GPIO.OUT)
    GPIO.setup(garbage_echoPin, GPIO.IN)
    GPIO.setup(recycle_trigPin, GPIO.OUT)
    GPIO.setup(recycle_echoPin, GPIO.IN)
    GPIO.setup(compost_trigPin, GPIO.OUT)
    GPIO.setup(compost_echoPin, GPIO.IN)

def capacity(bin):
    capacity = ((MAX_DISTANCE_BINS - bin) / MAX_DISTANCE_BINS) * 100
    return capacity
