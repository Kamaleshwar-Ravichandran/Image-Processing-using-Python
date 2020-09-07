import time
import numpy
import picamera
import cv2
import sys
import RPi.GPIO as GPIO
import matplotlib.image as img
import matplotlib.pyplot as plt


j=True;
iprefer=17;
ipstart=27;
ipreset=22;
ipstop=13;
optrue=10;
opfalse=9;
oprefer=11;


GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(17,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(27,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(22,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)

GPIO.output(oprefer,1)
i=0;
while i<10000:
    if GPIO.input(iprefer):
        with picamera.PiCamera() as camera:
            camera.start_preview()
            time.sleep(3)
           #camera.brightness=65
            camera.capture('/home/pi/Desktop/pics/pic1.jpg')
        GPIO.output(oprefer,0)
        break

    if GPIO.input(ipstop):
        j=False;
        
    GPIO.output(oprefer,1)
    i=i+1
    print i

    

GPIO.output(oprefer,0)

          
while j:
    GPIO.wait_for_edge(ipstart,GPIO.FALLING)
    with picamera.PiCamera() as camera:
        camera.capture('/home/pi/Desktop/pics/pic2.jpg')
   

    x=img.imread('pic1.jpg')
    y=img.imread('pic2.jpg')

    
    #z=plt.imshow(x)
    #plt.show()
    #z=plt.imshow(y)
    #plt.show()
    #gray1 = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
    #gray2 = cv2.cvtColor(y, cv2.COLOR_BGR2GRAY)
    #
    #plt.show()
    #a=(x==y);
    #a.all()

    
    roix1=x[136:172,214:249]
    roiy1=y[136:172,214:249]
    roix2=x[262:308,68:131]
    roiy2=y[262:308,68:131]
    #roix3=x[437:496,565:626]
    #roiy3=y[437:496,565:626]
    #roix4=x[105:240,751:820]
    #roiy4=y[105:240,751:820]

    
    #z=plt.imshow(roiy1)
    #plt.show()
    #z=plt.imshow(roiy2)
    #plt.show()
    #z=plt.imshow(roix3)
    #plt.show()
    #z=plt.imshow(roix4)
    #plt.show()
    

    
    ch1=((roix1-roiy1)<30)
    ch2=((roix1-roiy1)>160)
    ck1=ch1+ch2
    ck1=ck1.all()
    print ck1
    ch3=((roix2-roiy2)<30)
    ch4=((roix2-roiy2)>160)
    ck2=ch3+ch4
    ck2=ck2.all()
    print ck2
   # ch5=((roix3-roiy3)<30)
   # ch6=((roix3-roiy3)>160)
   # ck3=ch5+ch6
   # ck3=ck3.all()
   # print ck3
   # ch7=((roix4-roiy4)<30)
   # ch8=((roix4-roiy4)>160)
   # ck4=ch7+ch8
   # ck4=ck4.all()
   # print ck4
   
    if ((ck1==True)&(ck2==True)):     
        GPIO.output(optrue,1)
    else:
        GPIO.output(opfalse,1)

    time.sleep(2)
    GPIO.wait_for_edge(ipreset,GPIO.FALLING)
    GPIO.output(optrue,0)
    GPIO.output(opfalse,0)
    GPIO.output(oprefer,0)
    time.sleep(1)
    GPIO.output(optrue,1)
    GPIO.output(opfalse,1)
    GPIO.output(oprefer,1)
    time.sleep(2)
    GPIO.output(optrue,0)
    GPIO.output(opfalse,0)
    GPIO.output(oprefer,0)
    time.sleep(1)
    
    
