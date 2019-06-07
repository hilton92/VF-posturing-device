# Author: Benjamin Hilton
# Date: May 2019
# Stepper motor code used from:
# https://learn.adafruit.com/adafruits-raspberry-pi-lesson-10-stepper-motors/software
# Control for five-bar mechanism


import numpy as np
import math
import RPi.GPIO as GPIO
import Stepper


# multiplication by this rotation matrix transforms the right side origin into the base origin
T_d = np.array([[0.9063,-0.4226,26],[0.4226,0.9063,20],[0,0,1]])
# multiplication by this rotation matrix transforms the base origin to the right side origin
T_dINV = np.array([[0.9063,0.4226,-32.0164],[-0.4226,0.9063,-7.1381],[0,0,1]])
# multiplication by this rotation matrix transfroms the left side origin into the base origin
T_c = np.array([[0.9063,0.4226,-69.5028],[-0.4226,0.9063,40.2857],[0,0,1]])
# multiplication by this rotation matrix transforms the base origin to the left side origin
T_cINV = np.array([[0.9063,0.4226,-69.5028],[-0.4226,0.9063,40.2857],[0,0,1]])

GPIO.setmode(GPIO.BOARD)

# Declare stepper motors
StepperA_PUL = 47
StepperA_DIR = 49
StepperA_ENA = 51
StepperB_PUL = 46
StepperB_DIR = 48
StepperB_ENA = 50
StepperC_PUL = 39
StepperC_DIR = 41
StepperC_ENA = 43
StepperD_PUL = 38
StepperD_DIR = 40
StepperD_ENA = 42

LimitA_signal = 29
LimitB_signal = 27
LimitC_signal = 25
LimitD_signal = 23

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

GPIO.setup(LimitA_signal, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LimitB_signal, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LimitC_signal, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LimitD_signal, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



StepperA  = Stepper(StepperA_PUL, StepperA_DIR, StepperA_ENA, 488, LimitA_signal)
StepperB  = Stepper(StepperB_PUL, StepperB_DIR, StepperB_ENA, 336, LimitB_signal)
StepperC  = Stepper(StepperC_PUL, StepperC_DIR, StepperC_ENA, 512, LimitC_signal)
StepperD  = Stepper(StepperD_PUL, StepperD_DIR, StepperD_ENA, 527, LimitD_signal)

# Zero the Stepper Motors

StepperA.zero_stepper()
StepperB.zero_stepper()
StepperC.zero_stepper()
StepperD.zero_stepper()


while True:
     val = input("Enter X and Y in the form X_Y (no spaces)")
     X, Y = val.split("_",1)
    theta1, theta2 = transform(X,Y, )







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

    