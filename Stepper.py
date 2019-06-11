# Author: Benjamin Hilton
# Date: May 2019

import RPi.GPIO as GPIO
import time

class Stepper:
    def __init__(self, pul, dir, ena, steps, limitSwitch, direction, stepLimit, home):
        self.PULpin = pul
        self.DIRpin = dir
        self.ENApin = ena
        self.stepsFromZeroToHome = steps
        self.limitSwitchPin = limitSwitch
        self.direction = direction
        self.currentPosition = 0
        self.stepLimit = stepLimit
        self.stepsPerDegree = 14
        self.zeroPosition = -stepLimit - 100
        self.home = home
    
    def get_theta(self):
            theta = ((self.currentPosition - self.stepsFromZeroToHome) / self.stepsPerDegree) + self.home
            return theta
         
    
    def get_steps_from_theta_zero(self):
            return self.currentPosition - self.stepsFromZeroToHome
    
    def zero_stepper(self):
        while not GPIO.input(self.limitSwitchPin):
                self.take_steps(-1, 0.008)
        self.currentPosition = 0
        self.zeroPosition = 0
        self.take_steps(self.stepsFromZeroToHome, 0.008)


    def take_steps(self, steps, delay):
            
        if self.direction == 1:
                if self.currentPosition + steps > self.stepLimit or self.currentPosition + steps < self.zeroPosition:
                        print("Stepper has reached limit.")
                        return
                if steps > 0:
                        for x in range(steps):
                                GPIO.output(self.DIRpin, 0)
                                GPIO.output(self.ENApin, 1)
                                GPIO.output(self.PULpin, 1)
                                time.sleep(0.00005)
                                GPIO.output(self.PULpin, 0)
                                time.sleep(delay)
                        self.currentPosition = self.currentPosition + steps
                
                elif steps < 0:
                        steps = abs(steps)
                        for x in range(steps):
                                GPIO.output(self.DIRpin, 1)
                                GPIO.output(self.ENApin, 1)
                                GPIO.output(self.PULpin, 1)
                                time.sleep(0.00005)
                                GPIO.output(self.PULpin, 0)
                                time.sleep(delay) 
                        self.currentPosition = self.currentPosition - steps               
                
        
        elif self.direction == 0:
                if self.currentPosition + steps > self.stepLimit or self.currentPosition + steps < self.zeroPosition:
                        print("Stepper has reached limit.")
                        return
                if steps > 0:
                        for x in range(steps):
                                GPIO.output(self.DIRpin, 1)
                                GPIO.output(self.ENApin, 1)
                                GPIO.output(self.PULpin, 1)
                                time.sleep(0.00005)
                                GPIO.output(self.PULpin, 0)
                                time.sleep(delay)
                        self.currentPosition = self.currentPosition + steps
                
                elif steps < 0:
                        steps = abs(steps)
                        for x in range(steps):
                                GPIO.output(self.DIRpin, 0)
                                GPIO.output(self.ENApin, 1)
                                GPIO.output(self.PULpin, 1)
                                time.sleep(0.00005)
                                GPIO.output(self.PULpin, 0)
                                time.sleep(delay)  
                        self.currentPosition = self.currentPosition - steps

        




    
