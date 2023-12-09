import time
import RPi.GPIO as GPIO
import ultrasonic
import pygame
from webhook import send_webhook
import cv2
from picamera2 import Picamera2
from libcamera import Transform

# haarcascade and picamera init
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}, transform=Transform(vflip=1)))
picam2.start()

webhook_url = 'https://discord.com/api/webhooks/1180843360295067778/Qtzz-yuvcDb1h4hptWfLDprB_HWWlN4kz23082--97vZTj04gaJ804-G5uVDC2-CDU6V'

# Initialize the last sent notification time
g_last_notification_time = 0
r_last_notification_time = 0
c_last_notification_time = 0
notification_interval = 600  # 10 minutes in seconds

# leds, using gpio numbering
GPIO.setmode(GPIO.BOARD) # physical board numbering
red_garbage = 40
GPIO.setup(red_garbage, GPIO.OUT)
red_recycle = 38
GPIO.setup(red_recycle, GPIO.OUT)

red_recycle = 38
GPIO.setup(red_recycle, GPIO.OUT)

red_compost = 36
GPIO.setup(red_compost, GPIO.OUT)

if __name__ == '__main__':
    print("Starting...")
    time.sleep(1)
    ultrasonic.setup() # setups GPIO numbering and led
    pygame.mixer.init() # load music player
    pygame.mixer.music.load("Instructions.wav")

    current_time = time.time()
    message_played = False
    last_detection_time = 0
    t_end = time.time()

    try:
        while(True):
            im = picam2.capture_array()
            grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
            faces = face_detector.detectMultiScale(grey, 1.1, 3)
            print("Checking faces")
	
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))
                print("Face found!")
                
                if (not message_played or (current_time - last_detection_time) > 15): # Message is not replaying itself 15 second of last play
                    pygame.mixer.music.play() # plays instructions
                    time.sleep(3)
                    message_played = True
                    last_detection_time = current_time
                elif (message_played and (current_time - last_detection_time)):
                    message_played = False
            
            cv2.imshow("Faces", im)
            
            # check garbage every x seconds
            t_start = time.time()
            if (t_start >= t_end):
                garbage_bin = ultrasonic.getGarbageSonar()
                print(garbage_bin, "gbin")
                garbage_capacity = ultrasonic.capacity(garbage_bin)
                print("Garbage Bin Capacity is %.2f full"%(garbage_capacity))

                if (garbage_capacity > 70):
                    GPIO.output(red_garbage, GPIO.HIGH)
                    if (current_time - g_last_notification_time > notification_interval):
                        send_webhook(webhook_url, "Alert: Garbage bin is more than %.2f full. Please clear it."%(garbage_capacity))
                        g_last_notification_time = current_time
                else:
                    GPIO.output(red_garbage, GPIO.LOW)
                
                recycle_bin = ultrasonic.getRecycleSonar()
                recycle_capacity = ultrasonic.capacity(recycle_bin)
                print("Recycle Bin Capacity is %.2f full"%(recycle_capacity))

                if (recycle_capacity > 70):
                    GPIO.output(red_recycle, GPIO.HIGH)
                    if (current_time - r_last_notification_time > notification_interval):
                        send_webhook(webhook_url, "Alert: Recycle bin is more than %.2f full. Please clear it."%(recycle_capacity))
                        r_last_notification_time = current_time

                else:
                    GPIO.output(red_recycle, GPIO.LOW)
                
                compost_bin = ultrasonic.getCompostSonar()
                compost_capacity = ultrasonic.capacity(compost_bin)
                print("Capacity is %.2f full"%(compost_capacity))
                
                if (compost_capacity > 70):
                   GPIO.output(red_compost, GPIO.HIGH)
                   if (current_time - c_last_notification_time > notification_interval):
                       send_webhook(webhook_url, "Alert: Compost bin is more than %.2f full. Please clear it."%(compost_capacity))
                       c_last_notification_time = current_time
                else:
                    GPIO.output(red_compost, GPIO.LOW)
  
                t_end += 10
                
            time.sleep(0.5) # higher number cause delay on camera
                
    except KeyboardInterrupt:
        print("Exiting program...")
        
    finally:        
        GPIO.cleanup()
        cv2.destroyAllWindows()
