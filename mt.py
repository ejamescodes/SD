import time
import pigpio
import RPi.GPIO as GPIO
import sqlite3 as mydb
from time import sleep

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

con = mydb.connect('log/mtLog.db')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS mtLog(Date INTEGER, Motor_1 INTTEGER, Motor_2 INTEGER, Motor_3 INTEGER)""")

# if D is high it is clockwise and if it is low its counter-clockwise

#cannot set upper limit to more than 2500
def accel(D1, D2, D3, sig1, sig2, sig3, freq, accel, delay):
	with open("log/mtLog.csv", "a") as log:
		while freq != 2500:
			# Set direction
			pi.write(DIR1, D1)
			pi.write(DIR2, D2)
			pi.write(DIR3, D3)
			freq = freq + accel  # Increments frequency

			f1 = freq*sig1
			f2 = freq*sig2
			f3 = freq*sig3

			# Set frequency
			pi.set_PWM_frequency(STEP1, f1)
			pi.set_PWM_frequency(STEP2, f2)
			pi.set_PWM_frequency(STEP3, f3)

			# Output data to screen
			print (time.strftime('%Y-%m-%d %H:%M:%S')+" Motor 1 : %d HZ | Motor 2 : %d Hz| Motor 3 : %d Hz" %(f1, f2, f3))

			# Output data to csv
			log.write(time.strftime('%Y-%m-%d %H:%M:%S')+" Motor 1 : %d HZ | Motor 2 : %d Hz| Motor 3 : %d Hz" %(f1, f2, f3))

			# Logs data to database mtLog
			cur.execute('INSERT INTO mtLog (Date, Motor_1, Motor_2, Motor_3) VALUES(?,?,?,?)', (time.strftime('%Y-%m-%d %H:%M:%S'), f1, f2, f3))
			con.commit()

			sleep(delay)

#cannot set lower limit to less than 0
def maintain(D1, D2, D3, sig1, sig2, sig3, freq, delay):
	with open("log/mtLog.csv", "a") as log:
		# Set direction
		pi.write(DIR1, D1)
		pi.write(DIR2, D2)
		pi.write(DIR3, D3)

		f1 = freq*sig1
		f2 = freq*sig2
		f3 = freq*sig3

		# Set frequency
		pi.set_PWM_frequency(STEP1, f1)
		pi.set_PWM_frequency(STEP2, f2)
		pi.set_PWM_frequency(STEP3, f3)

		# Output data to screen
		print (time.strftime('%Y-%m-%d %H:%M:%S')+" Motor 1 : %d HZ | Motor 2 : %d Hz| Motor 3 : %d Hz" %(f1, f2, f3))

		# Output data to csv
		log.write(time.strftime('%Y-%m-%d %H:%M:%S')+" Motor 1 : %d HZ | Motor 2 : %d Hz| Motor 3 : %d Hz" %(f1, f2, f3))

		# Logs data to database mtLog 
		cur.execute('INSERT INTO mtLog (Date, Motor_1, Motor_2, Motor_3) VALUES(?,?,?,?)', (time.strftime('%Y-%m-%d %H:%M:%S'), f1, f2, f3))
		con.commit()

		sleep(delay)

#cannot set lower limit to less than 0
def decel(D1, D2, D3, sig1, sig2, sig3, freq, accel, delay):
	with open("log/mtLog.csv", "a") as log:
		while freq != 0:
			# Set direction
			pi.write(DIR1, D1)
			pi.write(DIR2, D2)
			pi.write(DIR3, D3)
			freq = freq - accel  # Increments frequency

			f1 = freq*sig1
			f2 = freq*sig2
			f3 = freq*sig3

			# Set frequency
			pi.set_PWM_frequency(STEP1, f1)
			pi.set_PWM_frequency(STEP2, f2)
			pi.set_PWM_frequency(STEP3, f3)

			# Output data to screen
			print (time.strftime('%Y-%m-%d %H:%M:%S')+" Motor 1 : %d HZ | Motor 2 : %d Hz| Motor 3 : %d Hz" %(f1, f2, f3))

			# Output data to csv
			log.write(time.strftime('%Y-%m-%d %H:%M:%S')+" Motor 1 : %d HZ | Motor 2 : %d Hz| Motor 3 : %d Hz" %(f1, f2, f3))

			# Logs data to database mtLog 
			cur.execute('INSERT INTO mtLog (Date, Motor_1, Motor_2, Motor_3) VALUES(?,?,?,?)', (time.strftime('%Y-%m-%d %H:%M:%S'), f1, f2, f3))
			con.commit()

			sleep(delay)

def move(direction1, direction2, direction3, signal1, signal2, signal3):
	F = 0 #frequency
	A = 50 #acceleration
	D = 50 #deceleration
	UL = 2500 #upper limit
	LL = 0 #lower limit
	DEL = 1/(2*(UL)/A) #delay

	# motor select lines
	s1 = 0
	s2 = 0
	s3 = 0
	if signal1 == GPIO.HIGH:
		s1 = 1
	else:
		s1 = 0

	if signal2 == GPIO.HIGH:
		s2 = 1
	else:
		s2 = 0

	if signal3 == GPIO.HIGH:
		s3 = 1
	else:
		s3 = 0

	lastState = 000
	state = (s1*100) + (s2*10) + s3

	if state == 000:
#		F = LL
#		accel(direction1, direction2, direction3, s1, s2, s3, F, A, DEL)

		F = UL
#		while state == 000:
		maintain(direction1, direction2, direction3, s1, s2, s3, F, DEL)

	elif state == 1:
#		F = LL
#		accel(direction1, direction2, direction3, s1, s2, s3, F, A, DEL)

		F = UL
#		while state == 1:
		maintain(direction1, direction2, direction3, s1, s2, s3, F, DEL)

	elif state == 10:
#		F = LL
#		accel(direction1, direction2, direction3, s1, s2, s3, F, A, DEL)

		F = UL
#		while state == 10:
		maintain(direction1, direction2, direction3, s1, s2, s3, F, DEL)

	elif state == 11:
#		F = LL
#		accel(direction1, direction2, direction3, s1, s2, s3, F, A, DEL)

		F = UL
#		while state == 11:
		maintain(direction1, direction2, direction3, s1, s2, s3, F, DEL)

	elif state == 100:
#		F = LL
#		accel(direction1, direction2, direction3, s1, s2, s3, F, A, DEL)

		F = UL
#		while state == 100:
		maintain(direction1, direction2, direction3, s1, s2, s3, F, DEL)

	elif state == 101:
#		F = LL
#		accel(direction1, direction2, direction3, s1, s2, s3, F, A, DEL)

		F = UL
#		while state == 101:
		maintain(direction1, direction2, direction3, s1, s2, s3, F, DEL)

	elif state == 110:
#		F = LL
#		accel(direction1, direction2, direction3, s1, s2, s3, F, A, DEL)

		F = UL
#		while state == 110:
		maintain(direction1, direction2, direction3, s1, s2, s3, F, DEL)

	elif state == 111:
#		F = LL
#		accel(direction1, direction2, direction3, s1, s2, s3, F, A, DEL)

		F = UL
#		while state == 111:
		maintain(direction1, direction2, direction3, s1, s2, s3, F, DEL)
	else:
		state = 000

#try:
#	S = GPIO.HIGH
	print ("test")
#	while True:
#		move(S,S,S,S,S,S)

#except KeyboardInterrupt:
#	print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
#	GPIO.cleanup()

#finally:
#	pi.set_PWM_dutycycle(STEP1, 0)  # PWM off
#	pi.stop()
