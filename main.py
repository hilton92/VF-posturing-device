# Author: Benjamin Hilton
# Date: May 2019
# Copyright 2019 Benjamin Hilton
# Control for five-bar mechanism


import numpy as np
import math

# Declare distances for geometry:
D_y = 20  # mm
D_x = 26  # mm
phiD_degrees = 25 #degrees
phiD = np.radians(phiD_degrees)
distBetweenActuators = 48 # mm


T_d = np.array([[np.cos(phiD),-np.sin(phiD), D_x], 
                [np.sin(phiD), np.cos(phiD), D_y], 
                [0,0,1]])

# Calculate inverse of T_d
Td_transpose = np.array([[np.cos(phiD),np.sin(phiD), 0], 
                [-np.sin(phiD), np.cos(phiD), 0], 
                [0,0,1]])

Td_translate = np.array([[1,0,-D_x],[0,1,-D_y],[0,0,1]])
T_dINV = np.dot(Td_transpose,Td_translate)

# Calculate left side from symmetry
phiC = phiD
farPoint = T_d * np.array([[distBetweenActuators],[0],[1]])
C_x = -farPoint(1)
C_y = farPoint(2)

T_c = np.array([[np.cos(-phiC),-np.sin(-phiC), C_x], 
                [np.sin(-phiC), np.cos(-phiC), C_y], 
                [0,0,1]])


# Calculate inverse of T_c
Tc_transpose = np.array([[np.cos(-phiC),np.sin(-phiC), 0], 
                [-np.sin(-phiC), np.cos(-phiC), 0], 
                [0,0,1]])

Tc_translate = np.array([[1,0,-C_x],[0,1,-C_y],[0,0,1]])
T_cINV = np.dot(Tc_transpose,Tc_translate)



# Arm Lengths:
lengthA = 5 # mm
lengthB = 5 # mm
lengthC = 47 # mm
lengthD = 64 # mm



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

    