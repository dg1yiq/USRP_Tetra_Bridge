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

Use:

Bridge between Tetra DMO Repeater (Motorola MTM5400) and Brandmeister DMR Network

Hardware:

Audio:    TETRA Radio <-> USB Soundcard <-> RaspberryPi
Serial:   TETRA Radio PEI Serial <-> RaspberryPi Serial Port
PTT:      TETRA Radio external PTT <-> RaspberryPi GPIO18

Callflow:

DMR <-> Tetra:

Brandmeister <-> DVSwitch <-> Analog_Bridge <-> USRP_Tetra_Bridge.py <-> Audio <-> TETRA Radio

USRP protocol settings:

The USRP_Tetra_Bridge.py is using the DVSwitch USRP protocol on the SAME host. So USRP inbound
and outbound ports needs to be different.

Check/modify following settings in /opt/Analog_Bridge/Analog_Bridge.ini

   [USRP]
   address = 127.0.0.1
   txPort = 31002
   rxPort = 31001

ALSA Audio Settimgs:

To use the correct Audio Interface (USB Soundcard) you have to make it default and check
for the correct input and output index number in functions "rxAudioStream()" and "txAudioStream()"
 
First Check 
