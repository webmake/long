#!/usr/bin/python
import serial
import time
from ccTalk import *

ser=serial.Serial('/dev/pts/2', 9600, timeout=1)

data = "";

def getMsg():
  msg = None
  while msg != None:
    data = data + ser.read(50)
    (data, msg) = parseMessages(data)
  return msg
  

def sendMessage(header, data='', source=1, destination=2):
    request = ccTalkMessage(header=header, payload=data, source=source,
    destination=destination)
    request.setPayload(header, data)
    ser.write(request)
    data = ser.read(50)
    messages = parseMessages(data)
    for message in messages:
        print messageit

init = ccTalkMessage()
init.setPayload(254)

ok = False

#Wait for device to be initiated
while ok!=True:
    ser.write(init.raw())
    data = ser.read(50)
    try:
        (data, messages) = parseMessages(data)
        response = messages[-1]
    except:
        continue
    if response.payload.header==0:
        ok = True
    else:
        print response.payload.header

#Set inhibit status to allow all
sendMessage(231,'\xff\xff')

#Set master inhibit status to enable device
sendMessage(228,'\x01')

#Read buffered credit or error codes
event = 0
while True:
    try:
        request = ccTalkMessage()
        request.setPayload(229)
        ser.write(request.raw())
        data = ser.read(50)
        messages = parseMessages(data)
        for message in messages:
            if message.payload.header==0:
                data = message.payload.data
                if ord(data[0])>event:
                    event = ord(data[0])
                    print "Counter  : " + str(ord(data[0]))
                    print "Credit 1 : " + str(ord(data[1])),
                    print "Error  1 : " + str(ord(data[2]))
                    print "Credit 2 : " + str(ord(data[3])),
                    print "Error  2 : " + str(ord(data[4]))
                    print "Credit 3 : " + str(ord(data[5])),
                    print "Error  3 : " + str(ord(data[6]))
                    print "Credit 4 : " + str(ord(data[7])),
                    print "Error  4 : " + str(ord(data[8]))
                    print "Credit 5 : " + str(ord(data[9])),
                    print "Error  5 : " + str(ord(data[10]))
        time.sleep(0.2)
    except KeyboardInterrupt, e:
        print "Quitting..."
        break
ser.close()
