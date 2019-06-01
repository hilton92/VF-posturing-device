# Author: Benjamin Hilton
# Date: May 2019
# Stepper motor code used from:
# https://learn.adafruit.com/adafruits-raspberry-pi-lesson-10-stepper-motors/software
# Control for five-bar mechanism


import numpy as np
import math
from gpiozero import Button # included with raspbian
import board # included with raspbian
import digitalio #from adafruit-blinka library, to install run "$ sudo pip3 install adafruit-blinka"

# multiplication by this rotation matrix transforms the right side origin into the base origin
T_d = np.array([[0.9063,-0.4226,26],[0.4226,0.9063,20],[0,0,1]])
# multiplication by this rotation matrix transforms the base origin to the right side origin
T_dINV = np.array([[0.9063,0.4226,-32.0164],[-0.4226,0.9063,-7.1381],[0,0,1]])
# multiplication by this rotation matrix transfroms the left side origin into the base origin
T_c = np.array([[0.9063,0.4226,-69.5028],[-0.4226,0.9063,40.2857],[0,0,1]])
# multiplication by this rotation matrix transforms the base origin to the left side origin
T_cINV = np.array([[0.9063,0.4226,-69.5028],[-0.4226,0.9063,40.2857],[0,0,1]])

# Declare stepper motors




while True:
    # zero stepper motors






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

    