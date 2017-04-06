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

wiringpi.wiringPiSetup()

receiver = RCSwitchReceiver()
receiver.enableReceive(2)

wiringpi.pinMode(27, 1) #green led
wiringpi.pinMode(28, 1) #red led
wiringpi.pinMode(29, 1) #yellow led

try: 
    while True:
    	if receiver.available():
            received_value = receiver.getReceivedValue()
            if received_value == armCode:
		subprocess.Popen(["/home/pi/codesend",str(armCode)])
		print("armed")
		process = subprocess.Popen(["python", "turnOnIOT433.py"], bufsize=0, shell=False)
		wiringpi.digitalWrite(27, 0) # turn off green led
	        wiringpi.digitalWrite(29, 1) #turn on yellow led
		time.sleep(3)
		wiringpi.digitalWrite(29, 0) #turn off yellow led
		wiringpi.digitalWrite(28, 1) #turn on red led
		recieved_value = 0
	    if received_value == disarmCode:
	    	#os.system("sudo killall node")
		subprocess.Popen(["/home/pi/codesend",str(disarmCode)])
		subprocess.Popen.kill(process)
		os.system("sudo killall node")
		#process.terminate()
		wiringpi.digitalWrite(28, 0) # turn off red led
		wiringpi.digitalWrite(29, 1) #turn on yellow led
		time.sleep(3)
		wiringpi.digitalWrite(29, 0) #turn off yellow led
	    	wiringpi.digitalWrite(27, 1) # turn on green led
		recieved_value = 0
#	    if received_value == alarmActivatedCode:
		#subprocess.Popen(["python", "picam.py"], bufsize=0, shell=True)
#		os.system("python /home/pi/picam.py")
    	receiver.resetAvailable()


except KeyboardInterrupt:  
    wiringpi.digitalWrite(27, 0) # turn off red led
    wiringpi.digitalWrite(28, 0) # turn off red led
    wiringpi.digitalWrite(29, 0) # turn off red led
