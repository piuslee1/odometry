# Odometry

## GPS
Plug 3 wires: Ground, 3.3V, and TX
On Board: Ground, 3.3V, and RX

Change port in gps.py accordingly

## BeagleBone Black
Linux Code to find IP: `avahi-browse -rat | grep -i -A 3 beaglebone`
or 192.168.6.2

To share internet over [usb](https://www.dangtrinh.com/2015/05/sharing-internet-with-beaglebone-black.html)
