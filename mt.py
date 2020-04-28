from time import sleep 
import pigpio 
import RPi.GPIO as GPIO

# Direction GPIO Pin
DIR1 = 19
DIR2 = 26
DIR3 = 20

 # Step GPIO Pin
STEP1 = 13
STEP2 = 16
STEP3 = 21

# Connect to pigpiod daemon
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR1, pigpio.OUTPUT)
pi.set_mode(DIR2, pigpio.OUTPUT)
pi.set_mode(DIR3, pigpio.OUTPUT)

pi.set_mode(STEP1, pigpio.OUTPUT)
pi.set_mode(STEP2, pigpio.OUTPUT)
pi.set_mode(STEP3, pigpio.OUTPUT)

MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
for i in range(3):
    	pi.write(MODE[i], RESOLUTION['Half'][i])


# Set duty cycle and frequency
pi.set_PWM_dutycycle(STEP1, 128)  # PWM 1/2 On 1/2 Off
pi.set_PWM_frequency(STEP1, 500)  # 500 pulses per second

pi.set_PWM_dutycycle(STEP2, 128)  # PWM 1/2 On 1/2 Off
pi.set_PWM_frequency(STEP2, 500)  # 500 pulses per second

pi.set_PWM_dutycycle(STEP3, 128)  # PWM 1/2 On 1/2 Off
pi.set_PWM_frequency(STEP3, 500)  # 500 pulses per second

#cannot set upper limit to more than 2500
def accel(Din, Dout, StepOut, freq, accel, delay):
	if freq != 2500
		pi.write(Dout, Din)  # Set direction
		freq = freq + accel  # Increments frequency
		pi.set_PWM_frequency(StepOut, freq) # Set frequency
		print(freq)
		sleep(delay)

#cannot set lower limit to less than 0
def maintain(Din, Dout, StepOut, freq, delay):
	pi.write(Dout, Din)  # Set direction
	pi.set_PWM_frequency(StepOut, freq) # Set frequency
	print(freq)
	sleep(delay)

#cannot set lower limit to less than 0
def decel(Din, Dout, StepOut, freq, decel, delay):
	if freq != 0:
		pi.write(Dout, Din)  # Set direction
		freq = freq - decel # Decrements frequency
		pi.set_PWM_frequency(StepOut, freq) # Set frequency
		print(freq)
		sleep(delay)

def move(direction1, direction2, direction3, signal1, signal2, signal3):
	F = 0 #frequency
	A = 50 #acceleration
	D = 50 #deceleration
	UL = 2500 #upper limit
	LL = 0 #lower limit
	DEL = 1/(2*(UL)/A) #delay
	F = LL
	accel(direction, F, A, DEL)
	F = UL
	maintain(direction, F, GPIO.HIGH, DEL)
	decel(direction, F, D, DEL)
	# motor select lines
	s1 = 0
	s2 = 0
	s3 = 0
	if signal1 == GPIO.HIGH:
		s1 = 100
	else:
		s1 = 0

	if signal2 == GPIO.HIGH:
		s2 = 10
	else:
		s2 = 0

	if signal3 == GPIO.HIGH:
		s3 = 1
	else: 
		s3 = 0 

	state = s1 + s2 + s3
	switch (state) {
		case 001:
		case 010:
		case 011:
		case 100:
		case 101:
		case 110:
		case 111:
		default:

try:
	D = GPIO.LOW

#	while True:
	move(D, 1)

except KeyboardInterrupt:
	print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
	GPIO.cleanup()

finally:
	pi.set_PWM_dutycycle(STEP1, 0)  # PWM off
	pi.stop()
