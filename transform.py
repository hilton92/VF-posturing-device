# Author: Benjamin Hilton
# Date: June 2019

import numpy as np
import math


# Function returns theta1 and theta2 in degrees
def transform(desiredX, desiredY):

    #print(desiredX)
    #print(desiredY)
    # Arm Lengths:
    lengthA = 5 # mm
    lengthB = 5 # mm
    lengthC = 47 # mm
    lengthD = 64 # mm
    lengthE = 7 # mm
    
    distBetweenActuators = 48 # mm

    lengthS = math.sqrt((distBetweenActuators-desiredX)**2 + desiredY**2)
    midAngle = np.arccos((lengthB**2 + (lengthD + lengthE)**2 - lengthS**2)/(2*lengthB*(lengthD+lengthE)))
    angle2_mod = np.arccos((lengthB**2 + lengthS**2 - (lengthD+lengthE)**2)/(2*lengthB*lengthS))
    angle4_mod = np.arcsin(desiredY/lengthS)
    angle5 =  3.1416 - angle4_mod - angle2_mod

    lengthR = math.sqrt(lengthD**2 + lengthB**2 - np.cos(midAngle)*2*lengthD*lengthB)
    angle2 = np.arccos((lengthB**2 + lengthR**2 - lengthD**2)/(2*lengthB*lengthR))
    angle4 = 3.1416 - angle5 - angle2
    
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
