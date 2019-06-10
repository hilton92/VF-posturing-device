# Author: Benjamin Hilton
# Date: June 2019

#~ from Stepper import Stepper
#~ import RPi.GPIO as GPIO

#~ GPIO.setmode(GPIO.BOARD)

#~ StepperA_PUL = 7
#~ StepperA_DIR = 5
#~ StepperA_ENA = 3


#~ LimitA_signal = 31


#~ GPIO.setup(StepperA_PUL, GPIO.OUT)
#~ GPIO.setup(StepperA_DIR, GPIO.OUT)
#~ GPIO.setup(StepperA_ENA, GPIO.OUT)


#~ GPIO.setup(LimitA_signal, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


#~ StepperA  = Stepper(StepperA_PUL, StepperA_DIR, StepperA_ENA, 488, LimitA_signal)


#~ # Zero the Stepper Motors

#~ StepperA.zero_stepper()

from transform import transform
import numpy as np

# multiplication by this rotation matrix transforms the base origin to the right side origin
T_dINV = np.array([[0.9063,0.4226,-32.0164],[-0.4226,0.9063,-7.1381],[0,0,1]])

while True:
    try:
        val = input("Enter X and Y in the form X,Y")
        myString = str(val)
        [X, Y] = myString.split(",")
    except KeyboardInterrupt:
        break
    except:
        print("That wasn't right. Try again")
        continue
    Y_base = int(Y) + 65
    XBaseRight = int(X)
    Right = np.dot(T_dINV, np.array([[XBaseRight],[Y_base],[1]]))
    theta1Right, theta2Right = transform(Right[0], Right[1])
            
    #convert to degrees
            
    theta1 = ((theta1Right / 3.1416) * 180) + 25
    theta2 = ((theta2Right / 3.1416) * 180) + 25
    print(theta1)
    print(theta2)
