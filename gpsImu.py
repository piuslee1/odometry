#!/usr/bin/env python2
import serial
import redis
import pynmea2

imuPort = "dev/ttyACM0"
gpsPort = "dev/tty0"


def main():
  print("Testing GPS")
  ser = serial.Serial(imuPort, 9600)
  print(ser.readline())
  gpsSer = serial.Serial(gpsPort, 9600)
  print(gpsSer.readline())
