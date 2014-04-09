#!/usr/bin/env python
# coding=UTF-8

import sys
import math, subprocess

p = subprocess.Popen(["ioreg", "-rc", "AppleSmartBattery"], stdout=subprocess.PIPE)
output = p.communicate()[0]

o_max = [l for l in output.splitlines() if 'MaxCapacity' in l][0]
o_cur = [l for l in output.splitlines() if 'CurrentCapacity' in l][0]
is_charging = [l for l in output.splitlines() if 'IsCharging' in l][0]
charger_connected = [l for l in output.splitlines() if 'ExternalConnected' in l][0]

color_green = '%{%F{green}%}'
color_yellow = '%{%F{yellow}%}'
color_red = '%{%F{red}%}'
color_reset = '%{[00m%}'

if "Yes" in charger_connected:
    if "Yes" in is_charging:
        sys.stdout.write(color_yellow + (u"⚡".encode('utf-8')))
else:
    b_max = float(o_max.rpartition('=')[-1].strip())
    b_cur = float(o_cur.rpartition('=')[-1].strip())

    charge = b_cur / b_max
    charge_threshold = float(10 * charge)

    # Output

    total_slots, slots = 10, []
    filled = float(math.ceil(charge_threshold * (total_slots / 10.0)))

    if filled >= 7.5:
        out = u'∷'
    elif filled >= 5:
        out = u'∴'
    elif filled >= 2.5:
        out = u'∶'
    else:
        out = u'⤬'

    color_out = (
        color_green if filled >= 7.5
        else color_yellow if filled >= 5
        else color_red
    )

    out = (color_out + out.encode('utf-8'))
    sys.stdout.write(out)
