# -*- coding: utf-8 -*-
#!/usr/bin/python3
""" Read output files """

import re
import pandas as pd
from io import StringIO
from os.path import exists
import numpy as np


class Field:
    def __init__(self):
        pass
    
    def add_subfield(self, name):
        self.__setattr__(name, Field())
    
    def add_item(self, name, value):
        self.__setattr__(name, value)    

# reading phits.out file
class Phits:
    def __init__(self, filename:str):
        assert exists(filename), 'Phits output file not found'
        self.filename = filename
        with open(filename, 'r') as f:
            content = f.read()
        
        template = r'prod. particles.+?\n-+?\n([a-zA-Z0-9\-\+\.\s]+?)\s+?-'
        string = re.findall(template, content)[0]
        self.prod = pd.read_csv(
            StringIO(string), 
            delim_whitespace=True, lineterminator='\n', header=None,
            names=['name', 'number', 'weight', 'weight_per_source']
            )
        
        template = r'leak. particles.+?\n.+?\n([a-zA-Z0-9\-\+\.\s]+?)\s+?-'
        string = re.findall(template, content)[0]
        self.leak = pd.read_csv(
            StringIO(string), 
            delim_whitespace=True, lineterminator='\n', header=None,
            names=['name', 'number', 'weight', 'weight_per_source']
            )

# T-cross reader (output forward current)
class ForwardCurrent:
    def __init__(self, filename:str):
        assert exists(filename), 'ForwardCurrent output file not found'
        self.filename = filename
        with open(filename, 'r') as f:
            content = f.read()
        
        template = (
                r'newpage:\s+#\s+no.+?([0-9]+).+?'
                r'e-lower.+?\n(.+?)\s+#.+?'
                r'space.+?\n\s+(.+?)\s*\n'
                r'\s+(\S+)\s+&=&\s+(\S+)\s+.+?\n'
                r'\s+(\S+)\s+&=&\s+(\S+)\s+.+?\n'
                r'\s+(\S+)\s+&=&\s+(\S+)\s+.+?\n'
                r'\s+(\S+)\s+&=&\s+(\S+)\s+.+?\ne:'
                )
        strings = re.findall(template, content, re.DOTALL)
        for p in strings:
            pname = 'page' + p[0]
            self.__setattr__(pname, Field())
            self.__dict__[pname].table = pd.read_csv(
                    StringIO(p[1]), 
                    delim_whitespace=True, lineterminator='\n', header=None,
                    names=['eLower', 'eUpper', 'proton', 'pErr', 'neutron', 'nErr']
                    )
            self.__dict__[pname].wt = Field()
            self.__dict__[pname].wt.title = p[2]
            self.__dict__[pname].wt.__setattr__(p[3], float(p[4]))
            self.__dict__[pname].wt.__setattr__(p[5], float(p[6]))
            self.__dict__[pname].wt.__setattr__(p[7], float(p[8]))
            self.__dict__[pname].wt.__setattr__(p[9], float(p[10]))
            
#T-Track with axis=xz
class TrackXZ:
    def __init__(self, filename:str):
        assert exists(filename), 'TrackXZ output file not found'
        self.filename = filename
        with open(filename, 'r') as f:
            content = f.read()
        
        template = (
                r'newpage:\s+#\s+no.+?([0-9]+).+?'
                r'#\s+nx\s+=(.+?)nz\s+=(.+?)\n#.+?'
                r'hc:\s+y\s+=(.+?)to(.+?)by(.+?);\s+'
                r'x\s+=(.+?)to(.+?)by(.+?);\n'
                r'(.+?)\n#.+?gshow.+?'
                r'space.+?(\w+)\s+&=&\s+(\S+)\s+.+?\n'
                r'\s+(\w+)\s+&=&\s+(\S+)\s+.+?\n'
                r'\s+(\w+)\s+&=&\s+(\S+)\s+.+?\n'
                r'\s+(\w+)\s+&=&\s+(\S+)\s+.+?\n'
                r'\s+(\w+)\.*\s+&=&\s+(\S+)\s+\ne:'
                )
        strings = re.findall(template, content, re.DOTALL)
        for p in strings:
            pname = 'page' + p[0]
            self.__setattr__(pname, Field())
            nx, ny = int(p[2]), int(p[1])
            self.__dict__[pname].ny   = ny
            self.__dict__[pname].nx   = nx
            self.__dict__[pname].ymax = float(p[3])
            self.__dict__[pname].ymin = float(p[4])
            self.__dict__[pname].dy   = float(p[5])
            self.__dict__[pname].xmin = float(p[6])
            self.__dict__[pname].xmax = float(p[7])
            self.__dict__[pname].dx   = float(p[8])
            self.__dict__[pname].hc = np.fromstring(
                p[9], dtype=float, sep=' ').reshape(nx, ny)
            self.__dict__[pname].wt = Field()
            self.__dict__[pname].wt.__setattr__(p[10], float(p[11]))
            self.__dict__[pname].wt.__setattr__(p[12], float(p[13]))
            self.__dict__[pname].wt.__setattr__(p[14], float(p[15]))
            self.__dict__[pname].wt.__setattr__(p[16], float(p[17]))
            self.__dict__[pname].wt.__setattr__(p[18], p[19])

# T-cross with mesh=reg
class CrossReg:
    def __init__(self, filename:str):
        assert exists(filename), 'CrossReg output file not found'
        self.filename = filename
        with open(filename, 'r') as f:
            content = f.read()
        
        template = (
                r'newpage:\s+#\s+no.+?([0-9]+).+?'
                r'e-lower.+?\n(.+?)\s+#.+?'
                r'space.+?\n\s+(.+?)\s*\n'
                r'\s+(\S+)\s+&=&\s+(\S+)\s+.+?\ne:'
                )
        strings = re.findall(template, content, re.DOTALL)
        for p in strings:
            pname = 'page' + p[0]
            self.__setattr__(pname, Field())
            self.__dict__[pname].table = pd.read_csv(
                    StringIO(p[1]), 
                    delim_whitespace=True, lineterminator='\n', header=None,
                    names=['eLower', 'eUpper', 'proton', 'pErr', 'neutron', 'nErr']
                    )
            self.__dict__[pname].wt = Field()
            self.__dict__[pname].wt.title = p[2]
            self.__dict__[pname].wt.__setattr__(p[3], float(p[4]))

# T-deposit with mesh=reg
class DepositReg:
    def __init__(self, filename:str):
        assert exists(filename), 'CrossReg output file not found'
        self.filename = filename
        with open(filename, 'r') as f:
            content = f.read()
        
        template = (
                r'newpage:\s+#\s+no.+?([0-9]+).+?'
                r'#\s+num.+?\n(.+?)\s+#\s+sum'
                )
        strings = re.findall(template, content, re.DOTALL)
        for p in strings:
            pname = 'page' + p[0]
            self.__setattr__(pname, Field())
            self.__dict__[pname].table = pd.read_csv(
                    StringIO(p[1]), 
                    delim_whitespace=True, lineterminator='\n', header=None,
                    names=['num', 'reg', 'volume', 'allpart', 'rErr']
                    )
# T-cross, output=fcurr, a-curr
class ForwardCurrentAngle:
    def __init__(self, filename:str):
        assert exists(filename), 'ForwardCurrentAngle output file not found'
        self.filename = filename
        with open(filename, 'r') as f:
            content = f.read()
        
        template = (
                r'newpage:\s+#\s+no.+?([0-9]+).+?'
                r'a-lower.+?\n(.+?)\s+#.+?'
                r'space.+?\n\s+(.+?)\s*\n'
                r'\s+(\S+)\s+&=&\s+(\S+)\s+.+?\n'
                r'\s+(\S+)\s+&=&\s+(\S+)\s+.+?\n'
                r'\s+(\S+)\s+&=&\s+(\S+)\s+.+?\n'
                r'\s+(\S+)\s+&=&\s+(\S+)\s+.+?\ne:'
                )
        strings = re.findall(template, content, re.DOTALL)
        for p in strings:
            pname = 'page' + p[0]
            self.__setattr__(pname, Field())
            self.__dict__[pname].table = pd.read_csv(
                    StringIO(p[1]), 
                    delim_whitespace=True, lineterminator='\n', header=None,
                    names=['aLower', 'aUpper', 'proton', 'pErr', 'neutron', 'nErr']
                    )
            self.__dict__[pname].wt = Field()
            self.__dict__[pname].wt.title = p[2]
            self.__dict__[pname].wt.__setattr__(p[3], float(p[4]))
            self.__dict__[pname].wt.__setattr__(p[5], float(p[6]))
            self.__dict__[pname].wt.__setattr__(p[7], float(p[8]))
            self.__dict__[pname].wt.__setattr__(p[9], float(p[10]))
