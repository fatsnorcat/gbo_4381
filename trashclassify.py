# import libraries
from gpiozero import LED
# from picamera import PiCamera
from time import *
# from lobe import ImageModel
import RPi.GPIO as GPIO
import ultrasonic
import pygame

# leds
green_garbage = LED(37)
red_garbage = LED(39)

# green_recycle = LED()
# red_recycle = LED()

# green_compost = LED()
# red_compost = LED()

# status_light = LED()

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
        green_garbage.on()
        sleep(10)
    # if (label == "recycle"):
    #     green_recycle.on()
    #     sleep(10)
    # if (label == "compost"):
    #     green_compost.on()
    #     sleep(10)
    else:
        green_garbage.off()
        # green_recycle.off()
        # green_compost.off()
        # status_light.off()

if __name__ == '__main__':
    print("Starting...")
    time.sleep(1)
    ultrasonic.setup() # setups GPIO numbering and led
    pygame.mixer.init() # load music player
    pygame.mixer.music.load("Instructions.m4a")
    try:
        while(True):
            main_dist = ultrasonic.getMainSonar()
            print("Object detected within %.2f cm"%(main_dist))
            if (main_dist < 500 & main_dist > 35):
                pygame.music.play() # sends instructions within 35 cm to 5m
                time.sleep(1)
            #     take_photo()
            #     result = model.predict_from_file('/home/pi/TrashClassifer/images/image.jpg')
            #     led_select(result.prediction)
            # else:
            #     status_light.pulse(2,1)
            #     sleep(1)
            garbage_bin = ultrasonic.getGarbageSonar()
            garbage_capacity = ultrasonic.capacity(garbage_bin)
            print("Capacity is %.2f full"%(garbage_capacity))
            if (garbage_capacity > 90):
                red_garbage.on()
            else:
                red_garbage.off()
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
            time.sleep(5) # wait 5 seconds
    except KeyboardInterrupt:
        GPIO.cleanup()