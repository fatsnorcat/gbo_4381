from picamera import PiCamera
from time import *
from lobe import ImageModel
import RPi.GPIO as GPIO
import ultrasonic
import pygame
from webhook import send_webhook

webhook_url = 'PASTE_WEBHOOK_URL_HERE'

# Initialize the last sent notification time
last_notification_time = 0
notification_interval = 600  # 10 minutes in seconds

# leds, using gpio numbering
GPIO.setmode(GPIO.BOARD) # physical board numbering
green_garbage = 31
GPIO.setup(green_garbage, GPIO.OUT)
red_garbage = 32
GPIO.setup(red_garbage, GPIO.OUT)

# green_recycle = 
# GPIO.setup(green_recycle, GPIO.OUT)
# red_recycle = 
# GPIO.setup(red_recycle, GPIO.OUT)

# green_compost = 
# GPIO.setup(green_compost, GPIO.OUT)
# red_compost = 
# GPIO.setup(red_compost, GPIO.OUT)

# status_light = LED()
# GPIO.setup(status_light, GPIO.OUT)

# camera = PiCamera()

# load lobe tf model
# model = ImageModel.load('/home/pi/Lobe/model')

def take_photo():
    status_light.on
    sleep(3)
    camera.start_preview(alpha=200)
    sleep(3)
    camera.capture('/home/pi/TrashClassifer/images')
    camera.stop_preview()
    sleep(1)

def led_select(label):
    print(label)
    if (label == "garbage"):
        GPIO.output(green_garbage, GPIO.HIGH)
        sleep(10)
    # if (label == "recycle"):
    #     GPIO.output(green_recycle, GPIO.HIGH)
    #     sleep(10)
    # if (label == "compost"):
        #     GPIO.output(green_compost, GPIO.HIGH)
    #     sleep(10)
    else:
        green_garbage.off()
        # green_recycle.off()
        # green_compost.off()
        # status_light.off()

if __name__ == '__main__':
    print("Starting...")
    sleep(1)
    ultrasonic.setup() # setups GPIO numbering and led
    pygame.mixer.init() # load music player
    pygame.mixer.music.load("Instructions.m4a")

    message_played = False
    last_detection_time = 0

    try:
        while(True):
            main_dist = ultrasonic.getMainSonar()
            current_time = time.time()

            print("Object detected within %.2f cm"%(main_dist))
            # Check if someone is within range
            if (35 < main_dist < 500):
                if (not message_played or (current_time - last_detection_time) > 15): # Message is not replaying itself 15 second of last play
                    pygame.music.play() # plays instructions
                    message_played = True
                    last_detection_time = current_time
            elif (message_played and (current_time - last_detection_time)):
                message_played = False
            #     take_photo()
            #     result = model.predict_from_file('/home/pi/TrashClassifer/images/image.jpg')
            #     led_select(result.prediction)
            # else:
            #     status_light.pulse(2,1)
            #     sleep(1)
            garbage_bin = ultrasonic.getGarbageSonar()
            garbage_capacity = ultrasonic.capacity(garbage_bin)
            print("Capacity is %.2f full"%(garbage_capacity))
            if (garbage_capacity > 80):
                GPIO.output(red_garbage, GPIO.HIGH)
                if (current_time - last_notification_time > notification_interval):
                    send_webhook(webhook_url, "Alert: Garbage bin is more than %.2f full. Please clear it."%(garbage_capacity))
                    last_notification_time = current_time
            else:
                GPIO.output(red_garbage, GPIO.LOW)
            # recycle_bin = ultrasonic.getRecycleSonar()
            # capacity = ultrasonic.capacity(recycle_bin)
            # print("Capacity is %.2f full"%(recycle_capacity))
            # if (recycle_capacity > 90):
            #     red_recycle.on()
            # else:
            #     red_recycle.off()
            # compost_bin = ultrasonic.getCompostSonar()
            # capacity = ultrasonic.capacity(compost_bin)
            # print("Capacity is %.2f full"%(compost_capacity))
            # if (compost_capacity > 90):
            #     red_compost.on()
            # else:
            #     red_compost.off()
            sleep(5) # wait 5 seconds
    except KeyboardInterrupt:
        GPIO.cleanup()
