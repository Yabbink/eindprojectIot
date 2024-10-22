#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://raspberrytips.nl

import sys
import time
import datetime
import RPi.GPIO as GPIO
import tm1637

#CLK -> GPIO23 (Pin 16)
#Di0 -> GPIO24 (Pin 18)

Display = tm1637.TM1637(13, 19, brightness=7)

Display.Clear()
Display.SetBrightness(1)

while(True):
   now = datetime.datetime.now()
   hour = now.hour
   minute = now.minute
   second = now.second
   currenttime = [ int(hour / 10), hour % 10, int(minute / 10), minute % 10 ]

   Display.Show(currenttime)
   Display.ShowDoublepoint(second % 2)

   time.sleep(1)
