#!/usr/bin/python

#espeak -vde "Hier ist das Tetra Relay DB0WMS in Schöppinge" --stdout | aplay --device=mycard

import RPi.GPIO as GPIO
from time import sleep
import subprocess

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)
sleep(1)
p = subprocess.Popen([r'./speak.sh'], stdout=subprocess.PIPE)
p.wait()
print (p.stdout.read())
GPIO.output(18, GPIO.LOW)
