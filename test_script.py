# Author: Benjamin Hilton
# Date: June 2019

from Stepper import Stepper
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

StepperA_PUL = 7
StepperA_DIR = 5
StepperA_ENA = 3


LimitA_signal = 31


GPIO.setup(StepperA_PUL, GPIO.OUT)
GPIO.setup(StepperA_DIR, GPIO.OUT)
GPIO.setup(StepperA_ENA, GPIO.OUT)


GPIO.setup(LimitA_signal, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


StepperA  = Stepper(StepperA_PUL, StepperA_DIR, StepperA_ENA, 488, LimitA_signal)


# Zero the Stepper Motors

StepperA.zero_stepper()

