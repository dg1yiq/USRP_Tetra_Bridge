#!/usr/bin/python
###################################################################################
# Copyright (C) 2014, 2015, 2016, 2017, 2018 N4IRR
#
# Tetra Modifikation Copyright (c) 2021 by DG1YIQ
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND ISC DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS.  IN NO EVENT SHALL ISC BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
###################################################################################

from time import sleep
import socket
import struct
import _thread
import pyaudio
import serial
import RPi.GPIO as GPIO

ipAddress = "127.0.0.1"

def rxAudioStream():
    global ipAddress
    print('Start RX audio thread')

    FORMAT = pyaudio.paInt16
    CHUNK = 320
    CHANNELS = 1
    RATE = 8000

    stream = p.open(format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    output = True,
                    frames_per_buffer = CHUNK,
                    output_device_index=3,
                    )

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    udp.bind(("", 31002))

    lastKey = -1
    call = ''
    tg = ''
    loss = '0.00%'
    rxslot = '0'
    while True:
        soundData, addr = udp.recvfrom(1024)
        if addr[0] != ipAddress:
            ipAddress = addr[0]
        if (soundData[0:4] == b'USRP'):
            eye = soundData[0:4]
            seq, = struct.unpack(">i", soundData[4:8])
            memory, = struct.unpack(">i", soundData[8:12])
            keyup, = struct.unpack(">i", soundData[12:16])
            talkgroup, = struct.unpack(">i", soundData[16:20])
            type, = struct.unpack("i", soundData[20:24])
            mpxid, = struct.unpack(">i", soundData[24:28])
            reserved, = struct.unpack(">i", soundData[28:32])
            audio = soundData[32:]
            if (type == 0): # voice
                if (len(audio) == 320):
                    stream.write(audio, 160)
                if (keyup != lastKey):
                    if keyup:
                        print ("(DMR -> Tetra) Transmission started...")
                        GPIO.output(18, GPIO.HIGH)
                        if call != '':
                           print ("(DMR -> Tetra) DMR Source-Call: %s" % call)
                    if keyup == False:
                        print ('(DMR -> Tetra) Transmission ended - Call %s Slot %s TG %s' % (call, rxslot, tg))
                        GPIO.output(18, GPIO.LOW)
                        call=''
                        tg = ''
                    lastKey = keyup
            if (type == 2): #metadata
                if audio[0] == 8:
                    tg = (audio[9] << 16) + (audio[10] << 8) + audio[11]
                    rxslot = audio[12];
                    call = audio[14:].decode('ascii')
        else:
            print("Invalid Packet")

    udp.close()

def txAudioStream():
    FORMAT = pyaudio.paInt16
    CHUNK = 320
    CHANNELS = 1
    RATE = 8000

    stream = p.open(format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK,
                    input_device_index=3,
                    )
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    lastPtt = ptt
    seq = 0
    while True:
        try:
            audio = stream.read(160, exception_on_overflow=False)
            if ptt != lastPtt:
                usrp = b'USRP' + struct.pack('>iiiiiii',seq, 0, ptt, 0, 0, 0, 0)
                udp.sendto(usrp, (ipAddress, 31001))
                seq = seq + 1
                if ptt==True:
                   print ('(Tetra -> DMR) Transmission started... ')
                if ptt==False:
                   print ('(Tetra -> DMR) Transmission ended. ')
            lastPtt = ptt
            if ptt:
                usrp = b'USRP' + struct.pack('>iiiiiii',seq, 0, ptt, 0, 0, 0, 0) + audio
                udp.sendto(usrp, (ipAddress, 31001))
                #print ('transmitting')
                seq = seq + 1
        except:
            print("overflow")

####
#### Hauptprogramm
####

ptt = False     # toggle this to transmit (left up to you)

ser = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)

p = pyaudio.PyAudio()

_thread.start_new_thread( rxAudioStream, () )
_thread.start_new_thread( txAudioStream, () )

print("Wit 3 Sec...")

sleep(1)
print("Switch to Repeater Mode")
ser.write(b'AT\r\n')
#Set CTOM=1 for DMO Mode or CTOM=6 for DMO Repeater Mode 
ser.write(b'AT+CTOM=6\r\n')

sleep(3)
print("Activaten Call Controll on PEI")
ser.write(b'AT+CTSP=2,0,0\r\n')

##root.mainloop()
while True:
   x=ser.readline()
   if x!=b'' and b'CDTXC' in x and ptt==True:
      print ("TETRA Squelch CLOSED")
      x=b''
      ptt=False
   if x!=b'' and b'CTXG: 1,3' in x :
      print ("TETRA Squelch OPEN")
      x=b''
      ptt=True
   if x!=b'':
      x=b''
