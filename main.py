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
        # Stepper(pulse pin, direction pin, enable pin, steps from limit switch to home, limit switch pin, direction, step limit, home (degrees))
        StepperA  = Stepper(StepperA_PUL, StepperA_DIR, StepperA_ENA, 675, LimitA_signal, 1, 1300, 45)
        StepperB  = Stepper(StepperB_PUL, StepperB_DIR, StepperB_ENA, 200, LimitB_signal, 1, 1300, 180)
        StepperC  = Stepper(StepperC_PUL, StepperC_DIR, StepperC_ENA, 200, LimitC_signal, 0, 1300, 180)
        StepperD  = Stepper(StepperD_PUL, StepperD_DIR, StepperD_ENA, 200, LimitD_signal, 0, 1300, 45)


        # Zero the Stepper Motors
        StepperA.zero_stepper()
        #StepperB.zero_stepper()
        #StepperC.zero_stepper()
        #StepperD.zero_stepper()
        
        
        #~ while True:
            #~ try:
                #~ val = input("Enter X and Y in the form X,Y")
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
            
            #~ print(Right[0])
            #~ print(Right[1])
            #~ theta1Right, theta2Right = transform(Right[0], Right[1])
            #~ theta1 = ((theta1Right / 3.1416) * 180) + 25
            #~ theta2 = ((theta2Right / 3.1416) * 180) + 25
            
            #~ print(theta1)
            #~ print(theta2)
    
    
            #~ stepsA = (theta2 - StepperA.get_theta()) * StepperA.stepsPerDegree
            #~ stepsB = (theta1 - StepperB.get_theta()) * StepperB.stepsPerDegree
            #~ stepsC = (theta1 - StepperC.get_theta()) * StepperC.stepsPerDegree
            #~ stepsD = (theta2 - StepperD.get_theta()) * StepperD.stepsPerDegree  
                      
            #~ for i in range(20): # take steps each stepper 1/20th of the way
                #~ StepperA.take_steps(int(stepsA / 20))
                #~ StepperB.take_steps(int(stepsB / 20))
                #~ StepperC.take_steps(int(stepsC / 20))
                #~ StepperD.take_steps(int(stepsD / 20))
                
            #~ # make any remaining movement
            #~ StepperA.take_steps(stepsA - StepperA.get_steps_from_theta_zero())
            #~ StepperB.take_steps(stepsB - StepperB.get_steps_from_theta_zero())
            #~ StepperC.take_steps(stepsC - StepperC.get_steps_from_theta_zero())
            #~ StepperD.take_steps(stepsD - StepperD.get_steps_from_theta_zero())
            #~ print("At X location " + str(X) + " and Y location " + str(Y))
                    
        
        
    except KeyboardInterrupt:
        # program was terminated
        print("Program terminated by user")
        
    finally:
        GPIO.cleanup()
        print("Cleaning up GPIO ports")











    
