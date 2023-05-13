# -*- coding: utf-8 -*-
#!/usr/bin/python3

from phits import InputFileGenerator, Title, Parameters, Source
from phits import Material, MatNameColor, Surface, Cell
from phits import T_Track, T_Cross_reg, T_Cross_rz, T_3Dshow


inFile = InputFileGenerator(
    Title, Parameters, Source, Material, MatNameColor, Surface, Cell,
    T_Track, T_Cross_reg, T_Cross_rz, T_3Dshow)
inFile.sec0.title = 'phits input file'
inFile.sec8.output = 'fcurr'
inFile.sec9.axis = 'z'
inFile.save('temp.inp')

