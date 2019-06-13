# Author: Benjamin Hilton
# Date: June 2019
# Function to perform trig on five-bar mechanism

import numpy as np
import math


# Function returns theta1 and theta2 in radians, given X and Y in five-bar origin (not base origin)
def transform(desiredX, desiredY):

    GE = desiredX
    GF = desiredY

    # Arm Lengths:
    ED = 5 # mm
    AB = 5 # mm
    DC = 47 # mm 
    BC = 64 # mm
    FC = 7 # mm
    
    EA = 48 # mm # Distance between actuators

    # Find geometry of triangle FBA
    FA = math.sqrt((EA-GE)**2 + GF**2)
    CBA = np.arccos((AB**2 + (BC + FC)**2 - FA**2)/(2*AB*(BC+FC)))
    FAB = np.arccos((AB**2 + FA**2 - (BC+FC)**2)/(2*AB*FA))
    FAE = np.arcsin(GF/FA)
    BAH =  3.1416 - FAE - FAB

    # Find geometry of triangle CBA
    CA = math.sqrt(BC**2 + AB**2 - np.cos(CBA)*2*BC*AB)
    BAC = np.arccos((AB**2 + CA**2 - BC**2)/(2*AB*CA))
    CAE = 3.1416 - BAH - BAC
    
    # Find geometry of triangle CDE
    KE = EA - np.arccos(CAE)*CA
    CK = np.sin(CAE)*CA
    EC = math.sqrt(KE**2 + CK**2)
    DEC = np.arccos((ED**2 + EC**2 - DC**2)/(2*ED*EC))
    CEA = np.arccos((EC**2 + EA**2 - CA**2)/(1*EC*EA))

    theta1 = DEC + CEA
    theta2 = BAH
    theta = [theta1, theta2]

    return theta
