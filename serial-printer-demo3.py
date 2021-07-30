#!/usr/bin/python
# make work with wav files
# increase baud
import sys
import time
import serial
import base64
import os
import wave


def encode(line):
    temp = base64.b64encode(bytes(str(line), encoding))
    temp = temp.decode("Ascii") + "\n"
    encoded = bytes(temp, encoding)
    return encoded

def upload(filename):
    ser.write(encode(filename))

    if ".txt" in filename or ".py" in filename:
        f = open(filename, "r")
        for line in f:
            encoded = encode(line)
            decoded = base64.b64decode(encoded)  # this and the following line are note necessary
            print("sending: " + decoded.decode("Ascii"), end="")
            ser.write(encoded)
            
    if ".wav" in filename:
        CHUNK = 1024
        wf = wave.open(filename, 'rb')
        data = wf.readframes(-1)
        print(data[0])
        for frame in data:
            ser.write(encode(frame))    
            print(frame)
        
        

    ser.write(bytes("*\n", encoding))
    
if __name__ == "__main__":
    n = len(sys.argv)
    if n < 2:
        print("usage: python3 " + sys.argv[0] + " filename1 ...")
        sys.exit()
    
    ser = serial.Serial(port='/dev/ttyUSB0',
                        baudrate=115200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=1)
    encoding = 'iso-8859-1'
    
    args = sys.argv[1:]
    for filename in args:
        upload(filename)
    
