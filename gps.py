#!/usr/bin/env python2
import serial
import pynmea2
import redis
from time import sleep

port = "/dev/ttyACM0"

def main_arduino():
	print("Running GPS Test Arduino")
	ser = serial.Serial(port, 9600)
	while True:
		try:
			gpsdat = ser.readline()
			print(ser.read(1))
			if gpsdat[0:6] == "$GPGGA":
				msg = pynmea2.parse(gpsdat)
				print("Lat: ",  msg.latitude)
				print("Long: ", msg.longitude)
		except Exception as e:
			print(e)
			return

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
	main_arduino()
