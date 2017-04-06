import os
import subprocess

with open(os.devnull, 'wb') as devnull:
   subprocess.check_call(['iot-433mhz', '-s /dev/ttyACM0'], stdout=devnull, stderr=subprocess.STDOUT)
