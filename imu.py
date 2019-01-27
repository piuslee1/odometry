import serial
import re
import redis
import pyquaternion as pyq
import sys
import os
import argparse

port = '/dev/cu.usbmodem14101'
file_name = os.path.abspath('mag.config')
s = serial.Serial(port,115200)
r = redis.Redis(host='localhost', port=6379, db=0)

def main():
    parser = argparse.ArgumentParser(description='IMU driver')
    parser.add_argument('--reset', help='Reset stored values.', action='store_true')
    args = parser.parse_args()

    if (args.reset):
        max_val_x = -9999
        max_val_y = -9999
        max_val_z = -9999

        min_val_x = sys.float_info.max
        min_val_y = sys.float_info.max
        min_val_z = sys.float_info.max

    elif (os.path.isfile(file_name)):
        file = open(file_name, 'r')
        max_vals = file.readline().split()
        max_val_x = float(max_vals[0])
        max_val_y = float(max_vals[1])
        max_val_z = float(max_vals[2])

        min_vals = file.readline().split()
        min_val_x = float(min_vals[0])
        min_val_y = float(min_vals[1])
        min_val_z = float(min_vals[2])
        
        file.close()
    else:
        raise AttributeError('Please set the [--reset] flag.')

    try:
        while True:
            line = str(s.readline())
            rec = None
            name = None

            if ("Accel" in line):
                rec = re.findall("-?\d+\.\d+", line)
                name = 'acceleration'

            if ("Mag" in line):
                rec = re.findall("-?\d+\.\d+", line)

                #Incoming values
                x = float(rec[0])
                y = float(rec[1])
                z = float(rec[2])

                #Maximum values so far
                max_val_x = max(max_val_x, x)
                max_val_y = max(max_val_y, y)
                max_val_z = max(max_val_z, z)

                #Minimum values so far
                min_val_x = min(min_val_x, x)
                min_val_y = min(min_val_y, y)
                min_val_z = min(min_val_z, z)

                if (max_val_x == min_val_x or
                    max_val_y == min_val_y or
                    max_val_z == min_val_z):
                    continue

                #Hard iron offset calculation
                offset_x = (max_val_x + min_val_x) / 2
                offset_y = (max_val_y + min_val_y) / 2
                offset_z = (max_val_z + min_val_z) / 2

                #Hard iron offset correction
                corrected_x = x - offset_x
                corrected_y = y - offset_y
                corrected_z = z - offset_z

                #Half-ranges
                avg_delta_x = (max_val_x - min_val_x) / 2
                avg_delta_y = (max_val_y - min_val_y) / 2
                avg_delta_z = (max_val_z - min_val_z) / 2

                #Range average
                avg_delta = (avg_delta_x + avg_delta_y + avg_delta_z) / 3

                #Multipliers
                scale_x = avg_delta / avg_delta_x
                scale_y = avg_delta / avg_delta_y
                scale_z = avg_delta / avg_delta_z

                #Soft iron scale adjustment
                corrected_x *= scale_x
                corrected_y *= scale_y
                corrected_z *= scale_z

                rec = [str(corrected_x),str(corrected_y),str(corrected_z)]
                name = 'orientation'

            if ("Gyro" in line):
                rec = re.findall("-?\d+\.\d+", line)
                name = 'rot_v'

            if (rec is not None):
                pub = rec[0] + ' ' + rec[1] + ' ' + rec[2]
                r.set(name, pub)
    except KeyboardInterrupt:
        if (args.reset):
            file = open(file_name, 'w')
            file.write(str(max_val_x) + ' ' + str(max_val_y) + ' ' + str(max_val_z) + '\n')
            file.write(str(min_val_x) + ' ' + str(min_val_y) + ' ' + str(min_val_z) + '\n')
            file.close()

if __name__ == "__main__":
    main()