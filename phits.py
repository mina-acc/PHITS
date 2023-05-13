# -*- coding: utf-8 -*-
#!/usr/bin/python3

from string import Formatter


class InputFileGenerator:
    def __init__(self, *args):
        for i,sec in enumerate(args):
            if issubclass(sec, Section):
                self.__dict__['sec'+str(i)] = sec()
                j = i + 1
            else:
                message = "InputFile object has no section '{}'".format(
                        sec.__name__
                        )
                raise AttributeError(message)
        self.__dict__['sec'+str(j)] = End()
    
    def __str__(self):
        return '\n'.join([str(v) for v in self.__dict__.values() if v])
    
    def __repr__(self):
        return self.__str__()    
    
    def save(self, path):
        with open(path, 'w') as f:
            f.write(self.__str__())


class Section:    
    def __init__(self):
        for _, fname, _, _ in Formatter().parse(self.__doc__):
            if fname:
                self.__dict__[fname] = None
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            if type(self.__dict__[name]) in [type(None), type(value)]:
                self.__dict__[name] = value
            else:
                message = "type mismatch: {} != {}".format(
                        type(self.__dict__[name]).__name__,
                        type(value).__name__
                        )
                raise ValueError(message)
        else:
            message = "'{}' section has no attribute '{}'".format(
                        self.__class__.__name__,
                        name
                        )
            raise AttributeError(message)
    
    def __str__(self):
        return self.__doc__.format(**self.__dict__)
    
    def __repr__(self):
        return self.__str__()
    

class Title(Section):
    """
file=phits.in
$OMP=4
[ T i t l e ]
{title}
    """
    def __init__(self):
        Section.__init__(self)
        self.title = 'untitled'


class Parameters(Section):
    """
[ P a r a m e t e r s ]
   file(1) = {file1: <10}      # (D=c:/phits) PHITS install folder name
   file(6) = {file6: <10}      # (D=phits.out) general output file name
     icntl = {icntl: <10}      # (D=0) 3:ECH 5:NOR 6:SRC 7,8:GSH 11:DSH 12:DUMP
    maxcas = {maxcas:<10}      # (D=10) number of particles per one batch
    maxbch = {maxbch:<10}      # (D=10) number of batches
     MDBATIMA = {MDBATIMA:<10}
    """
    def __init__(self):
        Section.__init__(self)
        self.file1  = 'c:/phits'
        self.file6  = 'phits.out'
        self.icntl  = 0
        self.maxcas = 100
        self.maxbch = 8
        self.MDBATIMA = 5000


class Source(Section):
    """
[ S o u r c e ]
    s-type = {stype: <10}     # mono-energetic axial source
      proj = {proj: <10}      # kind of incident particle         
       dir = {dir: <10}       # z-direction of beam [cosine]
        r0 = {r0: <10}        # radius [cm]
        z0 = {z0: <10}        # minimum position of z-axis [cm]
        z1 = {z1: <10}        # maximum position of z-axis [cm]
        e0 = {e0: <10}        # energy of beam [MeV/u]
    """
    def __init__(self):
        Section.__init__(self)
        self.stype = 1
        self.proj  = 'proton'
        self.dir   = 1.          
        self.r0    = 4.7            
        self.z0    = -20.            
        self.z1    = -20.            
        self.e0    = 2000.


class Material(Section):
    """
[ M a t e r i a l ]
mat[1]    {mat1: <10} 		# Beam pipe
mat[2]	  {mat2: <10}		# Target
mat[3]	  {mat3: <10}		# Moderator
mat[4]	  {mat4: <10}		# Shield
mat[5]    {mat5: <10}		# Reflector
    """
    def __init__(self, title='untitled'):
        Section.__init__(self)
        self.mat1 = 'Al  1.0'
        self.mat2 = 'W  1.0'
        self.mat3 = 'H  2.0  O  1.0'
        self.mat4 = 'B  4.0  C  1.0'
        self.mat5 = 'Be  1.0'


class MatNameColor(Section):
    """
[MatNameColor]
{name1:<10}     {color1: <10}
{name2:<10}     {color2: <10}
{name3:<10}     {color3: <10}
{name4:<10}     {color4: <10}
{name5:<10}     {color5: <10}
    """
    def __init__(self, title='untitled'):
        Section.__init__(self)
        self.name1 = '1 Aluminium-BeamPipe'
        self.color1 = 'darkgray'
        self.name2 = '2 Tungsten-Target'
        self.color2 = 'pastelmagenta'
        self.name3 = '3 Water-Moderator'
        self.color3 = 'pastelblue'
        self.name4 = '4 BoronCarbide-Shield'
        self.color4 = 'matblack'
        self.name5 = '5 Beryllium-Reflector'
        self.color5 = 'darkgreen'


class Surface(Section):
    """
[ S u r f a c e ]
    {no1: <10}     {type1: <10}     {dim1: <10}
    {no2: <10}     {type2: <10}     {dim2: <10}
    {no3: <10}     {type3: <10}     {dim3: <10}
    {no4: <10}     {type4: <10}     {dim4: <10}       $ target
    {no5: <10}     {type5: <10}     {dim5: <10} 
    {no6: <10}     {type6: <10}     {dim6: <10} 
    {no7: <10}     {type7: <10}     {dim7: <10} 
    """
    def __init__(self, title='untitled'):
        Section.__init__(self)
        self.no1 = 10
        self.type1 = 'so'
        self.dim1 = '12000.'
        self.no2 = 30
        self.type2 = 'pz'
        self.dim2 = '0.'
        self.no3 = 40
        self.type3 = 'pz'
        self.dim3 = '25.'
        self.no4 = 60
        self.type4 = 'cz'
        self.dim4 = '5.'
        self.no5 = 70
        self.type5 = 'cz'
        self.dim5 = '10.'
        self.no6 = 34
        self.type6 = 'pz'
        self.dim6 = '-5.'
        self.no7 = 35
        self.type7 = 'pz'
        self.dim7 = '13.'
        


class Cell(Section):
    """
[ C e l l ]
    {cellNo1: <10}    {matNo1: <10}    {matDensity1: <10}   $ Outer region
    {cellNo2: <10}    {matNo2: <10}    {matDensity2: <10}   #101 #102     $ Void
    {cellNo3: <10}    {matNo3: <10}    {matDensity3: <10}   $ Tungsten target	   	 	    
    {cellNo4: <10}    {matNo4: <10}    {matDensity4: <10}  #101   $ Moderator
    """
    def __init__(self, title='untitled'):
        Section.__init__(self)
        self.cellNo1 = 98
        self.matNo1 = -1
        self.matDensity1 = '10'
        self.cellNo2 = 300
        self.matNo2 = 0
        self.matDensity2 = '-10'
        self.cellNo3 = 101
        self.matNo3 = 2
        self.matDensity3 = '-19.3  -60  30  -40'
        self.cellNo4 = 102
        self.matNo4 = 3
        self.matDensity4 = '-1.0  -70  34  -35'

class T_Track(Section):
    """
[ T - T r a c k ]
     title = {title: <10}
      file = {file: <10}      # file name of output for the above axis
      mesh = {mesh: <10}      # mesh type is xyz scoring mesh
    x-type = {xtype: <10}     # x-mesh is linear given by xmin, xmax and nx
        nx = {nx: <10}        # number of x-mesh points
      xmin = {xmin: <10}      # minimum value of x-mesh points
      xmax = {xmax: <10}      # maximum value of x-mesh points
    y-type = {ytype: <10}     # y-mesh is given by the below data
        ny = {ny: <10}        # number of y-mesh points
      ymin = {ymin: <10}      # minimum value of y-mesh points
      ymax = {ymax: <10}      # maximum value of y-mesh points
    z-type = {ztype: <10}     # z-mesh is linear given by zmin, zmax and nz
        nz = {nz: <10}        # number of z-mesh points
      zmin = {zmin: <10}      # minimum value of z-mesh points
      zmax = {zmax: <10}      # maximum value of z-mesh points
      part = {part: <10}    
   2D-type = {_2Dtype: <10}   # 1:Cont, 2:Clust, 3:Color, 4:xyz, 5:mat, 6:Clust+Cont, 7:Col+Cont
    e-type = {etype: <10}     # e-mesh is given by the below data
        ne = {ne: <10}        # number of e-mesh points
             {energyMesh: <10}
      unit = {unit: <10}      # unit is [1/cm^2/source]
      axis = {axis: <10}      # axis of output
     gshow = {gshow: <10}     # 0: no 1:bnd, 2:bnd+mat, 3:bnd+reg 4:bnd+lat
    epsout = {epsout: <10}    # (D=0) generate eps file by ANGEL
    stdcut = {stdcut: <10} 
    """
    def __init__(self):
        Section.__init__(self)
        self.title  = 'Track in xyz mesh'
        self.file   = 't_xz.out'
        self.mesh   = 'xyz'
        self.xtype  = 2
        self.nx     = 100
        self.xmin   = -50.
        self.xmax   = 50.
        self.ytype  = 2
        self.ny     = 1
        self.ymin   = -0.5
        self.ymax   = 0.5
        self.ztype  = 2
        self.nz     = 100
        self.zmin   = -20.
        self.zmax   = 150.
        self.part   = 'proton neutron photon'
        self._2Dtype = 3
        self.etype  = 1
        self.ne     = 6
        self.energyMesh = '0.0 1e-9 1e-6 1e-3 1.0 1e3 2.5e3'
        self.unit   = 1
        self.axis   = 'xz'
        self.gshow  = 1
        self.epsout = 1
        self.stdcut = 0.01


class T_Cross_reg(Section):
    """
[ T - C r o s s ]
     title = {title: <10}
      file = {file: <10}      # file name of output for the above axis
      mesh = {mesh: <10}      # mesh type is region-wise
       reg = {reg: <10}       # number of crossing regions
             non     r-from    r-to    area
             {non1}  {rfrom1}  {rto1}  {area1}	
    e-type = {etype: <10}     # e-mesh is log given by emin, emax and ne
        ne = {ne: <10}        # number of e-mesh points
             {energyMesh: <10}
      unit = {unit: <10}      # unit is [1/cm^2/source]
      axis = {axis: <10}      # axis of output
    output = {output: <10}    # surface crossing flux
      part = {part: <10}   
    epsout = {epsout: <10}    # (D=0) generate eps file by ANGEL
    """
    def __init__(self, title='untitled'):
        Section.__init__(self)
        self.title  = 'Energy distribution in region mesh'
        self.file   = 'cross_reg.out'
        self.mesh   = 'reg'
        self.reg    = 1
        self.non1   = 1
        self.rfrom1 = 101
        self.rto1   = 99
        self.area1  = 1.
        self.etype  = 1
        self.ne     = 5
        self.energyMesh = '0.0  1e-6 1e-3 1.0 1e3 2e3'
        self.unit   = 1
        self.axis   = 'eng'
        self.output = 'flux'
        self.part   = 'proton neutron'
        self.epsout = 1


class T_Cross_rz(Section):
    """
[ T - C r o s s ]
     title = {title: <10}
      file = {file: <10}      # file name of output for the above axis
      mesh = {mesh: <10}      # mesh type is region-wise
    r-type = {rtype: <10}
      rmin = {rmin: <10}
      rmax = {rmax: <10}
        nr = {nr: <10}
    z-type = {ztype: <10}
      zmin = {zmin: <10}
      zmax = {zmax: <10}
        nz = {nz: <10}
    e-type = {etype: <10}     # e-mesh is log given by emin, emax and ne
        ne = {ne: <10}        # number of e-mesh points
             {energyMesh: <10}
      unit = {unit: <10}      # unit is [1/cm^2/source]
      axis = {axis: <10}      # axis of output
    output = {output: <10}    # surface crossing flux
      part = {part: <10}   
    epsout = {epsout: <10}    # (D=0) generate eps file by ANGEL
    stdcut = {stdcut: <10}
    """
    def __init__(self, title='untitled'):
        Section.__init__(self)
        self.title  = 'Energy distribution in r-z mesh'
        self.file   = 'cross_rz.out'
        self.mesh   = 'r-z'
        self.rtype  = 2
        self.rmin   = 0.
        self.rmax   = 437.44
        self.nr     = 1
        self.ztype  = 2
        self.zmin   = 5000.
        self.zmax   = 5001.
        self.nz     = 1
        self.etype  = 1
        self.ne     = 6
        self.energyMesh = '0.0 1e-9 1e-6 1e-3 1.0 1e3 2.5e3'
        self.unit   = 1
        self.axis   = 'eng'
        self.output = 'f-curr'
        self.part   = 'proton neutron'
        self.epsout = 1
        self.stdcut = 0.01


class T_3Dshow(Section):
    """
[ T - 3Dshow ]
     title = {title: <10}
      file = {file: <10}      # file name of output
    output = {output: <10}    # (D=3) 0:draft, 1:line, 2:col, 3:line+col
        x0 = {x0: <10}        # (D=0.0) x-coordinate of the origin
        y0 = {y0: <10}        # (D=0.0) y-coordinate of the origin
        z0 = {z0: <10}        # (D=0.0) z-coordinate of the origin
     e-the = {ethe: <10}      # (D=80.0) eye point theta(degree) from z-axis
     e-phi = {ephi: <10}      # (D=140.0) eye point phi(degree) from x-axis
     e-dst = {edst: <10}      # (D=w-dst*10) eye point distance from origin
     l-the = {lthe: <10}      # (D=e-the) light point theta from z-axis
     l-phi = {lphi: <10}      # (D=e-phi) light point phi from x-axis
     l-dst = {ldst: <10}      # (D=e-dst) light point distance from origin
     w-wdt = {wwdt: <10}      # (D=100) width of window (cm)
     w-hgt = {whgt: <10}      # (D=100) hight of window (cm)
     w-dst = {wdst: <10}      # (D=200) window distance from origin
    heaven = {heaven: <10}    # (D=y) direction to heaven
      line = {line: <10}      # (D=0) 0:surface+mat, 1:+region
    shadow = {shadow: <10}    # (D=0) 0:no, 1:shadow
     resol = {resol: <10}     # (D=1) resolution of 3dshow
    epsout = {epsout: <10}    # (D=0) generate eps file by ANGEL
   """
    def __init__(self, title='untitled'):
        Section.__init__(self)
        self.title  = 'Check geometry using [T-3dshow] tally'
        self.file   = '3dshow.out'
        self.output = 3
        self.x0     = 0.
        self.y0     = 0.
        self.z0     = 0.
        self.ethe   = 180.
        self.ephi   = 60.
        self.edst   = 500.
        self.lthe   = 150.
        self.lphi   = 30.
        self.ldst   = 100.
        self.wwdt   = 100.
        self.whgt   = 100.
        self.wdst   = 180.
        self.heaven = 0.
        self.line   = 1
        self.shadow = 2 
        self.resol  = 2
        self.epsout = 1


class End(Section):
    """
[ E n d ]
    """
    def __init__(self):
        Section.__init__(self)

        

    
    


