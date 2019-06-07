# Author: Benjamin Hilton
# Date: May 2019
# Control for five-bar mechanism


import numpy as np
import math
import RPi.GPIO as GPIO
from Stepper import Stepper


if __name__ == "__main__":

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
    StepperA  = Stepper(StepperA_PUL, StepperA_DIR, StepperA_ENA, 488, LimitA_signal)
    StepperB  = Stepper(StepperB_PUL, StepperB_DIR, StepperB_ENA, 336, LimitB_signal)
    StepperC  = Stepper(StepperC_PUL, StepperC_DIR, StepperC_ENA, 512, LimitC_signal)
    StepperD  = Stepper(StepperD_PUL, StepperD_DIR, StepperD_ENA, 527, LimitD_signal)


    # Zero the Stepper Motors
    #StepperA.zero_stepper()
    #StepperB.zero_stepper()
    StepperC.zero_stepper()
    #StepperD.zero_stepper()


#while True:
#    val = input("Enter X and Y in the form X_Y (no spaces)")
#    X, Y = val.split("_",1)
#    Y_base = Y + 50
#   XLeft = -X
#    XRight = X
#    theta1Left, theta2Left = transform(XLeft,Y_base)
#    theta1Right, theta2Right = transform(XRight, Y_base)






# Function returns theta1 and theta2 in degrees
def transform(desiredX, desiredY, distBetweenActuators):

    # Arm Lengths:
    lengthA = 5 # mm
    lengthB = 5 # mm
    lengthC = 47 # mm
    lengthD = 64 # mm


    lengthS = math.sqrt((distBetweenActuators-desiredX)**2 + desiredY**2)
    midAngle = np.arccos((lengthB**2 + (lengthD + lengthE)**2 - lengthS**2)/(2*lengthB*(lengthD+lengthE)))
    angle2_mod = np.arccos((lengthB**2 + lengthS**2 - (lengthD+lengthE)**2)/(2*lengthB*lengthS))
    angle4_mod = np.arcsin(desiredY/lengthS)
    angle5 =  -angle4_mod - angle2_mod

    lengthR = math.sqrt(lengthD**2 + lengthB**2 - np.cos(midAngle)*2*lengthD*lengthB)
    angle2 = np.arccos((lengthB**2 + lengthR**2 - lengthD**2)/(2*lengthB*lengthR))
    angle4 = 3.14159 - angle5 - angle2
    
    pivotX = distBetweenActuators - np.arccos(angle4)*lengthR
    pivotY = np.sin(angle4)*lengthR
    
    # Find length Q
    lengthQ = math.sqrt(pivotX**2 + pivotY**2)

    # Find angles of subtriangles
    angle1 = np.arccos((lengthA**2 + lengthQ**2 - lengthC**2)/(2*lengthA*lengthQ))
    
    angle3 = np.arcsin(pivotY/lengthQ)

    theta1 = angle3 + angle1
    theta2 = angle5
    
    theta = [theta1, theta2]

    return theta

    
