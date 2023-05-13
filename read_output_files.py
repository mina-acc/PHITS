# -*- coding: utf-8 -*-
#!/usr/bin/python3


""" Read output file: T100-phits.out """

import output_parser
import numpy as np
import matplotlib.pyplot as plt

root = './samples/'

phitsFile = output_parser.Phits(root + 'T100-phits.out')
fcurrFile = output_parser.ForwardCurrent(root + 'T100-fcurr.out')
txzFile   = output_parser.TrackXZ(root + 'T100-t_xz.out')

""" plot track_xz"""
Z = txzFile.page10.hc
x = np.arange(txzFile.page10.xmin, txzFile.page10.xmax, txzFile.page10.dx)  # len = 11
y = np.arange(txzFile.page10.ymin, txzFile.page10.ymax+1, txzFile.page10.dy)  # len = 7


fig, ax = plt.subplots()
pcm = ax.pcolormesh(x, y, Z)
fig.colorbar(pcm, ax=ax)

""" plot fcurr"""
# Data for plotting
eUpper = fcurrFile.page2.table.eUpper
neutron = fcurrFile.page2.table.neutron

fig, ax = plt.subplots()
ax.semilogx(eUpper, neutron)

ax.set(xlabel='energy (MeV)', ylabel='neutron current (1/source)',
       title='forward current')
ax.grid()

fig.savefig("test.png")
plt.show()