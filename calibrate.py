import os
import numpy
import cv2
import time
from pi5neo import Pi5Neo

radius=21
lights=350
neo = Pi5Neo('/dev/spidev0.0',lights,800, quiet_mode=True)
for i in range(lights):
    neo.set_led_color(i,255,255,255)
    neo.update_strip()
    time.sleep(1)
    os.system(f'fswebcam -r 1280x720 --no-banner --quiet ./image.jpg')
    image = cv2.imread('./image.jpg')
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (radius, radius), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    print(f'{i}: {maxVal}, {maxLoc}')
    neo.fill_strip(0,0,0)
    
