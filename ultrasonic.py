import RPi.GPIO as GPIO
import time

# pins
main_trigPin = 16
main_echoPin = 18
garbage_trigPin = 11
garbage_echoPin = 13
# recycle_trigPin = 1
# recycle_echoPin = 2
# compost_trigPin = 3
# compost_echoPin = 4

# size of bin
MAX_CAPACITY = 50 # height in cm

# max distance in cm for each ultrasonic sensor
MAX_DISTANCE_MAIN = 500
MAX_DISTANCE_BINS = 20
main_timeout = MAX_DISTANCE_MAIN * 60
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

# get measurement in cm
def getMainSonar():
    GPIO.output(main_trigPin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(main_trigPin, GPIO.LOW)
    pingTime = pulseIn(main_echoPin, GPIO.HIGH, main_timeout)
    distance = pingTime * 340.0 / 2.0 / 10000.0 # distance of sound speed 340m/s
    return distance

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
    GPIO.setmode(GPIO.BOARD) # physical board numbering
    GPIO.setup(main_trigPin, GPIO.OUT)
    GPIO.setup(main_echoPin, GPIO.IN)
    GPIO.setup(garbage_trigPin, GPIO.OUT)
    GPIO.setup(garbage_echoPin, GPIO.IN)
    # GPIO.setup(recycle_trigPin, GPIO.OUT)
    # GPIO.setup(recycle_echoPin, GPIO.IN)
    # GPIO.setup(compost_trigPin, GPIO.OUT)
    # GPIO.setup(compost_echoPin, GPIO.IN)

def loop():
    while(True):
        main_dist = getMainSonar()
        print("Motion detected within %.2f cm"%(main_dist))
        garbage_bin = getGarbageSonar()
        print("Capacity is %.2f cm high"%(garbage_bin))
        # recycle_bin = getRecycleSonar()
        # print("Capacity is %.2f cm high"%(recycle_bin))
        # compost_bin = getCompostSonar()
        # print("Capacity is %.2f cm high"%(compost_bin))
        time.sleep(5) # wait 5 second

def capacity(bin):
    capacity = (bin / MAX_CAPACITY) * 100
    return capacity