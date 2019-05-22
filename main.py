# Author: Benjamin Hilton
# Date: May 2019
# Copyright 2019 Benjamin Hilton
# Control for five-bar mechanism


import numpy as np

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

def transform():
    