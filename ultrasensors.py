# Allows for 4 ultrasonic sensors to work at the same time on a pi 4.
# Code is intended to work with a MC14051B CMOS Multiplexer IC by Motorola.
# Code is intended to work with 4 HC-SR04 ultrasonic sensors. Created to be scalable.
# Code for ultrasonic sensors referenced from: https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
# Code for use with Multiplexer referenced from: https://hackaday.io/project/165129-16-channel-thermocouple-multiplexer-for-raspi
# Spec sheet for the Multiplexer: https://www.onsemi.com/pub/Collateral/MC14051B-D.PDF
# Spec sheet for the Ultrasonic Sensor: https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf


# List of imports needed
import time
import os
import struct
import RPi.GPIO as GPIO
import time




GPIO.setmode(GPIO.BCM)

# Addressing all important things
TRIG      = 23
ECHO      = 24
MUX1_EN   = 31
FAULT     = 33
READY     = 29

# Mux Set up
def set_mux_address( address ):
    address = address & 0b00001111
    value = address & ( 1 << 3 )

    if ( value ):
        GPIO.output(MUX1_EN, GPIO.LOW)
    else:
        GPIO.output(MUX1_EN, GPIO.HIGH)

    value = address & ( 1 << 0 )
    if ( value ):
        GPIO.output(MUX_A0, GPIO.HIGH) 
    else:
        GPIO.output(MUX_A0, GPIO.LOW) 

def maincode( window ):
# Main Loop
    while True:
    
        print ("Measuring distance")

        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)

        GPIO.output(TRIG, false)
        print ("Waiting for sensor to settle")
        time.sleep(2)

        GPIO.output(TRIG, True)
        time.sleep(0.0001)
        GPIO.output(TRIG, False)

        # Times the pulses to determine distance.
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        # Math for the actual distance based on pulse time
        distance = pulse_duration * 17150

        distance = round(distance, 2)

    # The below code is an assumed distance of 10cm is an acceptable amount of space for direction correction.
    # Change the thresholds as testing permits.
    print ("Distance: ",distance," cm")
    if distance > 9:
        print ("This is a safe distance.")
    else:
        print ("This is an unsafe distance. Must move in a different direction.")