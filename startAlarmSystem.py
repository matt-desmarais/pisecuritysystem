# -*- coding: utf-8 -*-
#include <wiringPi.h>

from pi_switch import RCSwitchReceiver
import wiringpi
import time
import os
import subprocess

armCode = 5577987
disarmCode = 5577996
alarmActivatedCode = 11466866
lightCodeON = 5576451
lightCodeOFF = 5576460
isArmed = 0
alarm = 0

wiringpi.wiringPiSetup()

receiver = RCSwitchReceiver()
receiver.enableReceive(2)

wiringpi.pinMode(27, 1) #green led
wiringpi.pinMode(28, 1) #red led
wiringpi.pinMode(29, 1) #yellow led

def activateLight():
    time.sleep(5)
    subprocess.Popen(["/home/pi/codesend",str(lightCodeON)])
    return;

def alarmLightsON():
    wiringpi.digitalWrite(27, 1) # turn on green led
    wiringpi.digitalWrite(28, 1) # turn on red led
    wiringpi.digitalWrite(29, 1) # turn on yellow led
    
def alarmLightsOFF():
    wiringpi.digitalWrite(27, 0) # turn off green led
    wiringpi.digitalWrite(28, 0) # turn off red led
    wiringpi.digitalWrite(29, 0) # turn off yellow led

try: 
    while True:
    	if receiver.available():
            received_value = receiver.getReceivedValue()
            if(isArmed == 1):
		#motion sensor values 
		if(received_value == 6254489 or received_value == 9906905):
		    alarmLightsON()
		    activateLight()
		    alarm = 1
		#door sensors
		if(received_value == 8221033 or received_value == 7016089 or received_value == 7056121 or received_value == 7055961):
                    alarmLightsON()
		    activateLight()
		    alarm = 1
		#glass sensors
               #if(received_value == or received_value == or received_value == or received_value == ):
              #   alarmLightsON() 
	       #    activateLight()
		#    alarm = 1
	    if received_value == armCode:
		#resend arm code
		subprocess.Popen(["/home/pi/codesend",str(armCode)])
		print("armed")
		#turn on iot-433mhz
		process = subprocess.Popen(["python", "turnOnIOT433.py"], bufsize=0, shell=False)
		wiringpi.digitalWrite(27, 0) # turn off green led
	        wiringpi.digitalWrite(29, 1) #turn on yellow led
		time.sleep(3)
		wiringpi.digitalWrite(29, 0) #turn off yellow led
		wiringpi.digitalWrite(28, 1) #turn on red led
		recieved_value = 0
		isArmed = 1
	    if received_value == disarmCode:
		#turn off leds off
		if alarm:
      		    alarm = 0
		    alarmLightsOFF()
		#resend disarm code
		subprocess.Popen(["/home/pi/codesend",str(disarmCode)])
		subprocess.Popen.kill(process)
		#kill websever
		os.system("sudo killall node")
                subprocess.Popen(["/home/pi/codesend",str(lightCodeOFF)])
		wiringpi.digitalWrite(28, 0) # turn off red led
		wiringpi.digitalWrite(29, 1) #turn on yellow led
		time.sleep(3)
		wiringpi.digitalWrite(29, 0) #turn off yellow led
	    	wiringpi.digitalWrite(27, 1) # turn on green led
		recieved_value = 0
		isArmed = 0
#	    if received_value == alarmActivatedCode:
		#subprocess.Popen(["python", "picam.py"], bufsize=0, shell=True)
#		os.system("python /home/pi/picam.py")
    	receiver.resetAvailable()


except KeyboardInterrupt:  
    wiringpi.digitalWrite(27, 0) # turn off red led
    wiringpi.digitalWrite(28, 0) # turn off red led
    wiringpi.digitalWrite(29, 0) # turn off red led
