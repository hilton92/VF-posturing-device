# Author: Benjamin Hilton
# Date: May 2019
# Control for five-bar mechanism


import numpy as np
import math
import RPi.GPIO as GPIO
from Stepper import Stepper
from transform import transform


if __name__ == "__main__":

    try:

        # multiplication by this rotation matrix transforms the right side origin into the base origin
        T_d = np.array([[0.9063,-0.4226,26],[0.4226,0.9063,20],[0,0,1]])
        # multiplication by this rotation matrix transforms the base origin to the right side origin
        T_dINV = np.array([[0.9063,0.4226,-32.0164],[-0.4226,0.9063,-7.1381],[0,0,1]])
        # multiplication by this rotation matrix transfroms the left side origin into the base origin
        T_c = np.array([[0.9063,0.4226,-69.5028],[-0.4226,0.9063,40.2857],[0,0,1]])
        # multiplication by this rotation matrix transforms the base origin to the left side origin
        T_cINV = np.array([[0.9063,0.4226,-69.5028],[-0.4226,0.9063,40.2857],[0,0,1]])

        GPIO.setmode(GPIO.BOARD) # this means the numbers for buttons are specified by the board numbers (as opposed to processor numbers)

        # Declare stepper motors
        StepperA_PUL = 7
        StepperA_DIR = 5
        StepperA_ENA = 3
        StepperB_PUL = 11
        StepperB_DIR = 13
        StepperB_ENA = 15
        StepperC_PUL = 26
        StepperC_DIR = 24
        StepperC_ENA = 22
        StepperD_PUL = 40
        StepperD_DIR = 38
        StepperD_ENA = 36

        LimitA_signal = 31
        LimitB_signal = 33
        LimitC_signal = 35
        LimitD_signal = 37

        # Define all stepper control GPIO as output
        GPIO.setup(StepperA_PUL, GPIO.OUT)
        GPIO.setup(StepperA_DIR, GPIO.OUT)
        GPIO.setup(StepperA_ENA, GPIO.OUT)
        GPIO.setup(StepperB_PUL, GPIO.OUT)
        GPIO.setup(StepperB_DIR, GPIO.OUT)
        GPIO.setup(StepperB_ENA, GPIO.OUT)
        GPIO.setup(StepperC_PUL, GPIO.OUT)
        GPIO.setup(StepperC_DIR, GPIO.OUT)
        GPIO.setup(StepperC_ENA, GPIO.OUT)
        GPIO.setup(StepperD_PUL, GPIO.OUT)
        GPIO.setup(StepperD_DIR, GPIO.OUT)
        GPIO.setup(StepperD_ENA, GPIO.OUT)
        
        
        # Define all limit switch pins as inputs, enable built in pull down resistor
        GPIO.setup(LimitA_signal, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(LimitB_signal, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(LimitC_signal, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(LimitD_signal, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


        # Define stepper objects
        # Stepper(pulse pin, direction pin, enable pin, steps from limit switch to zero, limit switch pin)
        StepperA  = Stepper(StepperA_PUL, StepperA_DIR, StepperA_ENA, 1300, LimitA_signal, 1)
        StepperB  = Stepper(StepperB_PUL, StepperB_DIR, StepperB_ENA, 1000, LimitB_signal, 1)
        StepperC  = Stepper(StepperC_PUL, StepperC_DIR, StepperC_ENA, 1000, LimitC_signal, 0)
        StepperD  = Stepper(StepperD_PUL, StepperD_DIR, StepperD_ENA, 1000, LimitD_signal, 0)


        # Zero the Stepper Motors
        StepperA.zero_stepper()
        StepperB.zero_stepper()
        StepperC.zero_stepper()
        StepperD.zero_stepper()
        
        
        #~ while True:
            #~ try:
                #~ val = input("Enter X and Y in the form X,Y (no spaces)")
                #~ otherStrign = "hello"
                #~ myString = str(val)
                #~ [X, Y] = myString.split(",")
            #~ except KeyboardInterrupt:
                #~ break
            #~ except:
                #~ print("That wasn't right. Try again")
                #~ continue
            #~ Y_base = int(Y) + 65
            #~ XBaseRight = int(X)
            #~ Right = np.dot(T_dINV, np.array([[XBaseRight],[Y_base],[1]]))
            #~ theta1Right, theta2Right = transform(Right[0], Right[1])
            #~ stepsperdegree = 20
            #~ stepsA = theta1Left*stepsperdegree
            #~ stepsB = theta2Left*stepsperdegree
            #~ stepsC = theta1Right*stepsperdegree
            #~ stepsD = theta2Right * stepsperdegree
            #~ #StepperA.take_steps(stepsA)
            #~ #StepperB.take_steps(stepsB)
        
        
        
    except KeyboardInterrupt:
        # program was terminated
        print("Program terminated by user")
        
    finally:
        GPIO.cleanup()











    
