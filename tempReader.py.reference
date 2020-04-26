#Import Libraries we will be using
import RPi.GPIO as GPIO
import Adafruit_DHT as DHT
import time
import signal
import os
import sqlite3 as mydb
import sys

#Assign GPIO pins
tempPin = 17

#Temp and Humidity Sensor
tempSensor = DHT.DHT11
#LED Variables--------------------------------------------------------
#Duration of each Blink
blinkDur = .1
#Number of times to Blink the LED
blinkTime = 7
#---------------------------------------------------------------------
#Initialize the GPIO
GPIO.setmode(GPIO.BCM)

def oneBlink(pin):
	GPIO.output(pin,True)
	time.sleep(blinkDur)
	GPIO.output(pin,False)
	time.sleep(blinkDur)

def readF(tempPin):
	humidity, temperature = DHT.read_retry(tempSensor,17)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempFahr = '{0:0.1f}*F'.format(temperature)
	else:
		print('Error Reading Sensor')
	return tempFahr

con = mydb.connect('../log/tempLog.db')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS tempLog(Date INTTEGER, Temperature INTEGER)""")
data = 60
state = True
try:
#	with open("../log/tempLog.csv", "a") as log:
	while True:
#		os.system('clear')
#			print ("reading mock data")
		cur.execute('INSERT INTO tempLog (Date, Temperature) VALUES(?,?)', (time.strftime('%Y-%m-%d %H:%M:%S'), data))
		con.commit()
			#log.write("{0},{1}\n".format(time.strftime("%Y‐%m‐%d %H:%M:%S"),str(data)))
#		print (con.execute("SELECT * FROM tempLog"))
		print (data)
		if state == True:
			if data < 80:
				data+=5
			else: 
				state = False
		else:
			if data > 60:
				data-=5
			else:
				state = True
		time.sleep(60)

except KeyboardInterrupt:
	os.system('clear')
	print('Thanks for Blinking and Thinking!')
	GPIO.cleanup()
	con.close()
