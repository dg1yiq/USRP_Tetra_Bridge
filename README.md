Copyright (C) 2014, 2015, 2016, 2017, 2018 N4IRR

Tetra Modification Copyright (c) 2021 by DG1YIQ

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND ISC DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS.  IN NO EVENT SHALL ISC BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

## Use:

Bridge between Tetra DMO Repeater (Motorola MTM5400) and Brandmeister DMR Network

## Hardware:

Audio:    TETRA Radio <-> USB Soundcard <-> RaspberryPi
Serial:   TETRA Radio PEI Serial <-> RaspberryPi Serial Port
PTT:      TETRA Radio external PTT <-> RaspberryPi GPIO18

## Callflow:

DMR <-> Tetra:

Brandmeister <-> DVSwitch <-> Analog_Bridge <-> USRP_Tetra_Bridge.py <-> Audio <-> TETRA Radio

## USRP protocol settings:

The USRP_Tetra_Bridge.py is using the DVSwitch USRP protocol on the SAME host. So USRP inbound
and outbound ports needs to be different.

Check/modify following settings in /opt/Analog_Bridge/Analog_Bridge.ini

```
   [USRP]
   address = 127.0.0.1
   txPort = 31002
   rxPort = 31001
```

## ALSA Audio Settimgs:

To use the correct Audio Interface (USB Soundcard) you have to make it default and check
for the correct input and output index number in functions "rxAudioStream()" and "txAudioStream()"
 
First Check with command "aplay -l" the device number of you USB soundcard. Example with my
soundcard as "Karte 1" -> "Card 1":

```
Karte 1: Device [Generic USB Audio Device], Gerät 0: USB Audio [USB Audio]
  Sub-Geräte: 1/1
  Sub-Gerät #0: subdevice #0
```

Modify or create /etc/asound.conf as following:

```
pcm.!default {
    type hw
    card 1
}

ctl.!default {
    type hw           
    card 1
}

pcm.mycard {
    type plug
    slave { 
        pcm default 
        rate 44100
    }
}
```

This will set the USB Soundcard "Card 2" as default and create a PLUG Device with name "mycard"
(needed to transcode between different sample rates.

Restart RaspberryPi and check for the indey of created plug device "mycard", use this simple
Python script:

```
import pyaudio

po = pyaudio.PyAudio()
for index in range(po.get_device_count()): 
    desc = po.get_device_info_by_index(index)
    print ("DEVICE: {0} \t INDEX: {1} \t RATE: {2}".format(desc["name"],index,int(desc["defaultSampleRate"])))
```

Output will be like:

```
DEVICE: bcm2835 Headphones: - (hw:0,0) 	 INDEX: 0 	 RATE: 44100
DEVICE: Generic USB Audio Device: - (hw:1,0) 	 INDEX: 1 	 RATE: 44100
DEVICE: sysdefault 	 INDEX: 2 	 RATE: 44100
DEVICE: mycard 	 INDEX: 3 	 RATE: 44100
DEVICE: dmix 	 INDEX: 4 	 RATE: 48000
DEVICE: default 	 INDEX: 5 	 RATE: 44100
```

You will see that our created plug device "mycard" has index 3.

Modify USRP_Tetra_Bridge.py and add the correct output_device_index and input_device_index.

## Start System

Start DVSwitch

Start Script



