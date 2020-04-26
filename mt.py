from time import sleep 
import pigpio 
import RPi.GPIO as GPIO

DIR = 20     # Direction GPIO Pin
STEP = 21    # Step GPIO Pin
SWITCH = 16  # GPIO pin of switch

# Connect to pigpiod daemon
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)

# Set up input switch
pi.set_mode(SWITCH, pigpio.INPUT)
pi.set_pull_up_down(SWITCH, pigpio.PUD_UP)

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
pi.set_PWM_dutycycle(STEP, 128)  # PWM 1/2 On 1/2 Off
pi.set_PWM_frequency(STEP, 500)  # 500 pulses per second

#cannot set upper limit to more than 2500
def accel(dir, freq, accel, delay):
	while freq != 2500:
                        pi.write(DIR, dir)  # Set direction
                        freq = freq + accel
                        pi.set_PWM_frequency(STEP, freq)
                        print(freq)
                        sleep(delay)

#cannot set lower limit to less than 0
def decel(dir, freq, decel, delay):
        while freq != 0:
                        pi.write(DIR, dir)  # Set direction
                        freq = freq - decel
                        pi.set_PWM_frequency(STEP, freq)
                        print(freq)
                        sleep(delay)

def move(direction, time):
	F = 0 #frequency
	A = 50 #acceleration
	D = 50 #deceleration
	UL = 2500 #upper limit
	LL = 0 #lower limit
	DEL = time/(2*(UL)/A) #delay
	print(DEL)
	F = LL
	accel(direction, F, A, DEL)
	F = UL
	decel(direction, F, D, DEL)

try:
	D = GPIO.LOW

	while True:
		move(D, 1)

except KeyboardInterrupt:
	print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
	GPIO.cleanup()

finally:
	pi.set_PWM_dutycycle(STEP, 0)  # PWM off
	pi.stop()
