#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xtrack as xt
import xobjects as xo
import scipy




# %%
lcirc = 1000.0
lquad = 3.0
lbend = 5.0
max_dipole_field = 3.0
number_of_FODO = 8
pc_GeV = 20.0

lFODO = lcirc/number_of_FODO
theta_max = max_dipole_field*lbend/(3.3356*pc_GeV)
min_number_of_dipoles = round((2.0*np.pi)/theta_max)
# %%
number_of_dipoles = 32
number_of_dipoles_per_FODO = number_of_dipoles/number_of_FODO
# %%

target_bmax = 300.0
def fun(f, L, target):
    return 2*f*np.sqrt(4*f+L)/np.sqrt(4*f-L) - target


f_0 = scipy.optimize.root(fun, 100, args=(lFODO, target_bmax))['x'][0]
f_0
# %%
f = np.linspace(125/4+1,200, 1000)
plt.plot(f, fun(f, lFODO, target_bmax)+target_bmax,'b',lw=3)
plt.grid(True)
plt.xlabel('f [m]')
plt.ylabel('$\\beta_{MAX}$ [m]')
# %%

k1 = 1.0/f_0/lquad
k1


#%%
env = xt.Environment()
env.vars({'lFODO': lFODO, 
          'lquad': lquad, 
          'lbend': lbend, 
          'k1f': k1, 
          'k1d': -k1,
          'number_of_dipoles': number_of_dipoles,
          'angle.mb': 2.0*np.pi/number_of_dipoles,
          'k0.mb': 'angle.mb/lbend',
          })

lcirc = 1000.0
lquad = 3.0
lbend = 5.0
max_dipole_field = 3.0
number_of_FODO = 8
pc_GeV = 20.0

env.new('mb', xt.Bend, length='lbend', k0='k0.mb', h='k0.mb')
#env.new('mb', xt.Multipole, knl=['k0.mb', 0.0], hxl='k0.mb')
env.new('mq', xt.Quadrupole, length='lquad')

env.new('mq.f', 'mq', k1='k1f')
env.new('mq.d', 'mq', k1='k1d')

cell = env.new_line(components=[
    env.place('mq.f', at=lquad*0.5),
    env.place('mb', at=18.75 + lbend*0.5),
    env.place('mb', at=43.75 + lbend*0.5),
    env.place('mq.d', at=62.5 + lquad*0.5),
    env.place('mb', at=81.25 + lbend*0.5),
    env.place('mb', at=106.25 + lbend*0.5),
    env.new('marker_end', xt.Marker, at=lFODO),

])

cell.to_pandas()

#%%

cells = env.new_line(components=[
    env.new('start', xt.Marker),
    cell,
    env.new('end', xt.Marker),
])

#%% append in cells number_of_FODO times cell
line = env.new_line(components=[env.place(cell)]*number_of_FODO)

line.to_pandas()


# %%
# 2. Definition of the beam
line.particle_ref = xt.Particles(p0c=6500e9, #eV
                                 q0=1, mass0=xt.PROTON_MASS_EV)
# %%
context = xo.ContextCpu()
line.build_tracker(_context=context)

#%%
mySurvey = line.survey()
mySurvey = mySurvey.rows[r'^(mq|mb).*']
fig, ax = plt.subplots(figsize=(9, 6))
plt.plot(mySurvey.X, mySurvey.Z, 'o-', label="x", c="k")
plt.axis('square')
plt.xlabel('X [m]')
plt.ylabel('Z [m]')
plt.grid()
# %%
myTwiss= line.twiss(method='4d')

#%%
# The closed orbit corresponds in this case to the reference orbit
plt.subplot(211)
plt.plot(myTwiss.s,myTwiss.x,'b',label='x')
plt.ylabel('x [m]')
plt.grid()
plt.ylim(-0.05,0.05)

plt.subplot(212)
plt.plot(myTwiss.s,myTwiss.y,'r',label='y')
plt.xlabel('s [m]')
plt.ylabel('y [m]')
plt.grid()
plt.ylim(-0.05,0.05)

#%%
def plot_me(myTwiss):
    plt.plot(myTwiss.s,myTwiss.betx,'.-b', label='betx')
    plt.plot(myTwiss.s,myTwiss.bety,'.-r', label='bety')
    plt.ylabel('[m]')
    plt.xlabel('s [m]')
    plt.grid()
    plt.legend()

    plt.figure()
    plt.plot(myTwiss.s,myTwiss.alfx,'.-b', label='alfx')
    plt.plot(myTwiss.s,myTwiss.alfy,'.-r', label='alfx')
    plt.xlabel('s [m]')
    plt.ylabel('')
    plt.grid()
    plt.legend()

    plt.figure()
    plt.plot(myTwiss.s,myTwiss.mux,'.-b', label='mux')
    plt.plot(myTwiss.s,myTwiss.muy,'.-r', label='muy')
    plt.xlabel('s [m]')
    plt.ylabel('2pi')
    plt.grid()
    plt.legend()

    plt.figure()
    plt.plot(myTwiss.s,myTwiss.dx,'.-b', label='dx')
    plt.plot(myTwiss.s,myTwiss.dy,'.-r', label='dy')
    plt.xlabel('s [m]')
    plt.ylabel('[m]')
    plt.grid()
    plt.legend()
plot_me(myTwiss)




# %%
