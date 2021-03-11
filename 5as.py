import glob
import serial
import sys
import time
# import os
import traceback
import json

usb_ttys = glob.glob("/dev/ttyUSB*")
port = usb_ttys[0]

ser = serial.Serial()
ser.port = port
ser.baudrate = 9600
ser.bytesize = 8
ser.parity = 'N'
ser.stopbits = 1
ser.timeout = 1 # read timeout

def readint():
    readbyte = ser.read(1)
    if readbyte == b'':
        return None
    readbyte = int.from_bytes(readbyte, byteorder='big')
    print("< "+hex(readbyte))
    return readbyte




ser.open()
if not ser.is_open:
    print("Failed to open serial port")
    sys.exit(1)

print(ser)
readbyte = readint() # just read to clear the line

# wait for 00, 00 from the programmer trying to wake us up
data = []
while True:
    readbyte = readint()
    if readbyte is not None:
        data.append(readbyte)
        if len(data) >= 2 and data[-1] == b'\x00' and data[-2] == b'\x00':
            break

# looks like we got 2 breaks, reply to programmer
time.sleep(0.309) # sniffed as 309ms pause from the 5as
ser.write(b'\x55')
time.sleep(0.007)
ser.write(b'\x83')
time.sleep(0.007)
ser.write(b'\x76') # maybe f6/f7 too depending on what the programmer tries

print("waiting for next data from programer")
while True:
    readbyte = ser.read(1)
    if readbyte != b'':
        print(readbyte.hex())
