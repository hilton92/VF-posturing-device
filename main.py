# Author: Benjamin Hilton
# Date: May 2019
# Control for posturing device (five-bar mechanism)


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

        # Declare limit switches
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
        StepperA  = Stepper(StepperA_PUL, StepperA_DIR, StepperA_ENA, 450, LimitA_signal, 1, 1300, 45)
        StepperB  = Stepper(StepperB_PUL, StepperB_DIR, StepperB_ENA, 400, LimitB_signal, 1, 1300, 180)
        StepperC  = Stepper(StepperC_PUL, StepperC_DIR, StepperC_ENA, 320, LimitC_signal, 0, 1300, 180)
        StepperD  = Stepper(StepperD_PUL, StepperD_DIR, StepperD_ENA, 450, LimitD_signal, 0, 1300, 45)


        # Zero the Stepper Motors
        print("Zeroing stepper motors...")
        StepperA.zero_stepper()
        StepperB.zero_stepper()
        StepperC.zero_stepper()
        StepperD.zero_stepper()

        
        while True:
            try:
                val = input("Enter X and Y in the form X,Y")
                myString = str(val)
                [X, Y] = myString.split(",")
            except KeyboardInterrupt:
                break
            except:
                print("That wasn't right. Try again.")
                continue
            Y_base = float(Y) + 65
            XBaseRight = float(X)

            # Transform points from base origin to right-side origin
            Right = np.dot(T_dINV, np.array([[XBaseRight],[Y_base],[1]]))

            # Calculate degrees of actuators for requested X and Y
            theta1Right, theta2Right = transform(Right[0], Right[1])

            # Convert to degrees, add 25 (transform function returns theta in right-side origin, add 25 to get in base origin)
            theta1 = ((theta1Right / 3.1416) * 180) + 25
            theta2 = ((theta2Right / 3.1416) * 180) + 25
            
    
            # Calculate required steps for move
            stepsA = math.floor((theta2 - StepperA.get_theta()) * StepperA.stepsPerDegree)
            stepsB = math.floor((theta1 - StepperB.get_theta()) * StepperB.stepsPerDegree)
            stepsC = math.floor((theta1 - StepperC.get_theta()) * StepperC.stepsPerDegree)
            stepsD = math.floor((theta2 - StepperD.get_theta()) * StepperD.stepsPerDegree)  
            
            # Separate movement into [factor] separate movements
            factor = 20
            steps_a = math.floor(stepsA / factor)
            remainder_a = stepsA % factor
            steps_b = math.floor(stepsB / factor)
            remainder_b = stepsB % factor
            steps_c = math.floor(stepsC / factor)
            remainder_c = stepsC % factor
            steps_d = math.floor(stepsD / factor)
            remainder_d = stepsD % factor
            
            ##########
            
            #CHANGE THIS VARIABLE TO MAKE THE DEVICE MOVE FASTER (doesn't affect zeroing speed)
            delay = 0.001 # 0.0001 is the smallest this should be (smaller is faster)
            
            ##########
            
            # Take steps each stepper 1 /[factor] of the way          
            for i in range(factor):
                StepperA.take_steps(steps_a, delay)
                StepperB.take_steps(steps_b, delay)
                StepperC.take_steps(steps_c, delay)
                StepperD.take_steps(steps_d, delay)

                
            # make any remaining movement
            StepperA.take_steps(remainder_a, delay)
            StepperB.take_steps(remainder_b, delay)
            StepperC.take_steps(remainder_c, delay)
            StepperD.take_steps(remainder_d, delay)
            print("At X location " + str(X) + " and Y location " + str(Y))
                    
        
        
    except KeyboardInterrupt:
        # Program was terminated by user (CTRL C)
        print("Program terminated by user")
        
    finally:
        # Runs even if error occurs, cleanup resets all GPIO pins as inputs and frees them for other use
        GPIO.cleanup()
        print("Cleaning up GPIO ports")











    
