#!/usr/bin/env python

import serial, time

# This is the Publisher

uno = serial.Serial('/dev/tty96B0', 9600)
uno.write('')
time.sleep(5)

print('Off.')
uno.write('\x02')
uno.write('\x20')
uno.write('\x00')
uno.write('\x00')
uno.write('\x00')
uno.write('\x00')
uno.write('\x00')
uno.write('\x00')
uno.write('\x00')
uno.write('\xFF')

time.sleep(10)

print('SelfTest')
uno.write('\x02')
uno.write('\x10')
uno.write('\x00')
uno.write('\x00')
uno.write('\x00')
uno.write('\x00')
uno.write('\x00')
uno.write('\x00')
uno.write('\x00')
uno.write('\xFF')

time.sleep(10)

print('LED to GREEN %')
uno.write('\x02')
uno.write('\x30')
uno.write('\x04')
uno.write('\x00')
uno.write('\xFF')
uno.write('\x00')
uno.write('\xFF')
uno.write('\x00')
uno.write('\x00')
uno.write('\xFF')

time.sleep(10)

print('Progress bar')
uno.write('\x02')
uno.write('\x40')
uno.write('\x50')
uno.write('\xFF')
uno.write('\x00')
uno.write('\x00')
uno.write('\xFF')
uno.write('\x00')
uno.write('\x00')
uno.write('\xFF')

