# Listen for activation signal and then trigger servo to open vending machine
# Data received from Azure IoT Hub

# Written by: Reece Gounden

import sys
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)

import signal
from datetime import datetime,timedelta
import time
import binascii
import requests
import os

# Startup set date and time
def SetCurrentDateTime():
    response = requests.get('http://worldclockapi.com/api/json/utc/now',
		    headers={'content-type':'application/json; charset=utf-8'})
    sdate = response.content[30:40]
    stime = response.content[41:46]
    cmd = "sudo date -s \"{0} {1} UTC\"".format(sdate,stime)

    os.system(cmd)
    
SetCurrentDateTime()

# Dictionary to look up tray number
trayDict = {
    "1" : 03,
    "2" : 05,
    "3" : 07,
    "4" : 11,
    "5" : 13
}

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(03, GPIO.OUT)
GPIO.setup(05, GPIO.OUT)
GPIO.setup(07, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)


# Set 'angle' of servo on 'pin'
def SetAngle(angle, pin):
    pwm=GPIO.PWM(pin, 50)
    pwm.start(0)
    duty = angle / 18 + 2
    GPIO.output(pin, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(pin, False)
    pwm.ChangeDutyCycle(0)
    pwm.stop()

# Dispense a drink from tray
def DispenseDrink(tray):
    if tray is not None:
        print('***Dispensing an ice cold beverage***') 
        pin = trayDict[tray];
        if tray is "3":  #tray 3 is weird so it requires different angles
            SetAngle(140,pin) #140
            SetAngle(50,pin) #50
        else:
            SetAngle(180,pin) #160
            SetAngle(90,pin) #90
	

def main():
    
    print('''\
         __                              ___   __        .ama     ,
      ,d888a                          ,d88888888888ba.  ,88"I)   d
     a88']8i                         a88".8"8)   `"8888:88  " _a8'
   .d8P' PP                        .d8P'.8  d)      "8:88:baad8P'
  ,d8P' ,ama,   .aa,  .ama.g ,mmm  d8P' 8  .8'        88):888P'
 ,d88' d8[ "8..a8"88 ,8I"88[ I88' d88   ]IaI"        d8[         
 a88' dP "bm8mP8'(8'.8I  8[      d88'    `"         .88          
,88I ]8'  .d'.8     88' ,8' I[  ,88P ,ama    ,ama,  d8[  .ama.g
[88' I8, .d' ]8,  ,88B ,d8 aI   (88',88"8)  d8[ "8. 88 ,8I"88[
]88  `888P'  `8888" "88P"8m"    I88 88[ 8[ dP "bm8m88[.8I  8[
]88,          _,,aaaaaa,_       I88 8"  8 ]P'  .d' 88 88' ,8' I[
`888a,.  ,aadd88888888888bma.   )88,  ,]I I8, .d' )88a8B ,d8 aI
  "888888PP"'        `8""""""8   "888PP'  `888P'  `88P"88P"8m"
    ''')
    
    
    #variable to store the value of tray to be dispensed
    tray = None
    
    try:
	tray = sys.argv[1] 
	print("Dispensing from tray number: ", tray)
    except Exception:
	print "No tray input arguments, waiting for SignalR tray dispense message..."
    
    #wait for async dispense tray message
    
    #Dispense drink

   
    
    
    DispenseDrink(tray)
    #DispenseDrink("5")
    #DispenseDrink("4")
    #DispenseDrink("3")
    #DispenseDrink("2")
    #DispenseDrink("1")
    GPIO.cleanup()
    

if __name__ == "__main__":
    main()    
