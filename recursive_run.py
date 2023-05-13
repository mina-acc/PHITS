# -*- coding: utf-8 -*-
#!/usr/bin/python

root = '/home/lqm/Desktop/omid/NeutronRange/' 
phitsexe = '/opt/PHITS/phits/bin/phits323_lin_mpi.exe'
rootPython = '/home/lqm/Desktop/omid/Python_Templates/'

import sys
sys.path.append(rootPython)

from phits import InputFileGenerator, Title, Parameters, Source
from phits import Material, MatNameColor, Surface, Cell
from phits import T_Track, T_Cross_reg, T_Cross_rz, T_3Dshow
import output_parser
import subprocess
import numpy as np
import os



nEnergy = [0.001, 0.01, 0.1, 1., 10.]

mat  = {'Au':['Au',
                 '-19.3  -60  30  -40',
                 'Au  1.0',
                 '2 Gold-Target'],
       'Hg':['Hg',
                 '-13.53  -60  30  -40',
                 'Hg  1.0',
                 '2 Mercury-Target'],
       'Pb':['Pb',
                 '-11.34  -60  30  -40',
                 'Pb  1.0',
                 '2 Lead-Target'], 
        'Ta':['Ta',
                 '-16.65  -60  30  -40',
                 'Ta  1.0',
                 '2 Talium-Target'], 
         'U':['U',
                 '-19.1  -60  30  -40',
                 'U  1.0',
                 '2 Uranium-Target'], 
       }



for label,value in mat.items():
	TargetLength = 5.0
	for neutronEnergy in nEnergy:
		inFile = InputFileGenerator(
			 Title, Parameters, Source, Material, MatNameColor,
			 Surface, Cell, T_Track, T_Cross_rz)
		inFile.sec1.maxcas = 100000
		inFile.sec2.proj = 'neutron'
		inFile.sec2.e0 = neutronEnergy
		inFile.sec5.dim3  = TargetLength
		inFile.sec5.dim4 = '50.0'
		inFile.sec6.matDensity3 = value[1]
		inFile.sec3.mat2  = value[2]
		inFile.sec4.name2 = value[3]
		inFile.sec8.ne = 1
		inFile.sec8.energyMesh = '0.0 2.5e3'


		while True:
			path = root + label + '/' + str(neutronEnergy) + 'MeV' + '/' + str(TargetLength) + 'cm' + '/'
			os.makedirs(path, exist_ok=True)
			os.chdir(path)
			inFile.save(path + 'phits.in')

			bashCommand =  ['mpirun -np 45 '+ phitsexe]
			print('Target Material:', label,'Target Length:', TargetLength, 'Neutron Energy:', neutronEnergy)
			process = subprocess.Popen(bashCommand, shell=True,
									   stdout=subprocess.PIPE,
									   stderr=subprocess.PIPE,
									   universal_newlines=True
									   )
			
			stdoutFile = open(path + 'stdout.txt', 'a')
			stderrFile = open(path + 'stderr.txt', 'a')
			while process.poll() is None:
				stdout = process.stdout.readline()
				stderr = process.stderr.readline()
				print(stdout.rstrip())
				stdoutFile.write(stdout)
				stderrFile.write(stderr)
				
			stdoutFile.close()
			stderrFile.close()

			fcurrFile = output_parser.ForwardCurrent(path + 'cross_rz.out')
			if ((fcurrFile.page1.table.neutron[0]*fcurrFile.page1.wt.area > 0.001) and (fcurrFile.page1.table.nErr[0] < 0.1)):
			   TargetLength = TargetLength + 5.0
			   inFile.sec5.dim3  = TargetLength
			else:
				break
			
#			phitsFile = output_parser.Phits(path + 'phits.out')
#			LeakNeutronIndex = np.where(phitsFile.leak.name =='neutron')
#			LeakNeutron = phitsFile.leak.weight_per_source[LeakNeutronIndex[0]]
#			if LeakNeutron[LeakNeutronIndex[0][0]] > 0.001:
#			   TargetLength = TargetLength + 5.0
#			   inFile.sec5.dim3  = TargetLength
#			else:
#				break





