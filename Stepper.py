# Author: Benjamin Hilton
# Date: May 2019

import RPi.GPIO as GPIO
import time

class Stepper:
    def __init__(self, pul, dir, ena, steps, limitSwitch):
        self.PULpin = pul
        self.DIRpin = dir
        self.ENApin = ena
        self.stepsFromZeroToStarting = steps
        self.limitSwitchPin = limitSwitch
    
    def zero_stepper(self):
        while not GPIO.input(self.limitSwitchPin):
            self.take_steps(-1)
        self.currentPosition = 0
        self.take_steps(20)


    def take_steps(self, steps):
        if steps > 0:
            for x in range(steps):
                GPIO.output(self.DIRpin, 0)
                GPIO.output(self.ENApin, 1)
                GPIO.output(self.PULpin, 1)
                time.sleep(0.00005)
                GPIO.output(self.PULpin, 0)
                time.sleep(0.005)
        
        elif steps < 0:
            steps = abs(steps)
            for x in range(steps):
                GPIO.output(self.DIRpin, 1)
                GPIO.output(self.ENApin, 1)
                GPIO.output(self.PULpin, 1)
                time.sleep(0.00005)
                GPIO.output(self.PULpin, 0)
                time.sleep(0.001)                







    
