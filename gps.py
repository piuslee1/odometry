#!/usr/bin/env python2
import serial
import pynmea2
import redis
from time import sleep

port = "/dev/ttyS0"

def main():
	print("Running GPS Test")
	ser = serial.Serial(port, 9600)
	while True:
		try:
			gpsdat = ser.readline()
			if gpsdat[0:6] == "$GPGGA":
				msg = pynmea2.parse(gpsdat)
				print("Lat: ",  msg.latitude)
				print("Long: ", msg.longitude)
		except Exception as e:
			print(e)
			return

if __name__ == '__main__':
	main()
