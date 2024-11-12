#%%
import xtrack as xt
import numpy as np
import matplotlib.pyplot as plt
import xobjects as xo
import matplotlib.patches as patches

#%%
pc_GeV = 20.0

circum = 2000.0 # circumference
ncell = 40 # number of cells
lcell = circum/ncell # length of cell
lq=3.0 # length of quadrupole
number_dipoles_percell = 4
theta = (2.0*np.pi)/ncell/number_dipoles_percell
k1 = 0.0098 # quadrupole strength
lsex = 0.00001


env = xt.Environment()
env.vars({'lcell': lcell, 
          'lq': lq,
          'theta': theta,
          'kf': k1,
          'kd': -k1,
          'kfl': k1*lq,
          'kdl': -k1*lq,
          'lsex': lsex,
          'ksf': 0.0,
            'ksd': 0.0,
          })

#env.new('mb', xt.Bend, k0='theta', h='theta')
env.new('mb', xt.Multipole, knl=['theta', 0, 0], hxl='theta')
env.new('mqf', xt.Multipole, knl=[0, "kfl", 0])
env.new('mqd', xt.Multipole, knl=[0, "kdl", 0])
env.new("msf", xt.Multipole, knl=[0, 0, "ksf"])
env.new("msd", xt.Multipole, knl=[0, 0, "ksd"])



cell = env.new_line(components=[
    env.place('mqf', at=0),
    env.place('msf', at=lsex*0.5),
    env.place('mb', at=0.15*lcell),
    env.place('mb', at=0.35*lcell),
    env.place("mqd", at=0.5*lcell),
    env.place('msd', at=0.5*lcell + lsex*0.5),
    env.place('mb', at=0.65*lcell),
    env.place('mb', at=0.85*lcell),
    env.new('marker_end', xt.Marker, at=lcell),
])

cell.to_pandas()


#%%

cells = env.new_line(components=[
    env.new('start_cell', xt.Marker),
    cell,
    env.new('end_cell', xt.Marker),
])

#%% append in cells number_of_FODO times cell
line = env.new_line(components=[env.place(cells)]*ncell)

line.to_pandas()


# %%
# 2. Definition of the beam
line.particle_ref = xt.Particles(p0c=pc_GeV*1e9, #eV
                                 q0=1, mass0=xt.PROTON_MASS_EV)
# %%
context = xo.ContextCpu()
line.build_tracker(_context=context)
#%%

mytwiss = line.twiss(method="4d")

#%%
def plotLatticeSeries(ax,mys, length, height=1., v_offset=0., color='r',alpha=0.5,lw=3):

    ax.add_patch(
    patches.Rectangle(
        (mys, v_offset-height/2.),   # (x,y)
        length,          # width
        height,          # height
        color=color, alpha=alpha,lw=lw
    )
    )
    return;

def useful_plots(transfer_line, tw1, ylim1=None, ylim2=None, ylim3=None, filter_elements="ThinSliceQuadrupole"):
    fig = plt.figure(figsize=(13,8))

    ax1=plt.subplot2grid((3,3), (0,0), colspan=3, rowspan=1)

    #plt.grid()
    color = 'red'
    ax1.set_ylabel('1/f=K1L [m$^{-1}$]', color=color)  # we already handled the x-label with ax1
    ax1.tick_params(axis='y', labelcolor=color)
    if ylim1 is not None:
        plt.ylim(ylim1[0], ylim1[1])
    else:
        plt.ylim(-.08,.08)
    #plt.ylim(-2,2)


    plt.title('Exercise 5')
    quads_table = transfer_line.get_table().rows[transfer_line.get_table().element_type ==  filter_elements] #
    for quad in quads_table.name:
        k1l = transfer_line.get_strengths().rows[quad].k1l[0] 
        aux = tw1.rows[quad].s[0]
        #print(quad, k1l) #transfer_line.get(quad)
        try:
            length = transfer_line.get(quad).length
        except:
            length=0
        plotLatticeSeries(plt.gca(),aux, length, height=k1l, v_offset=k1l/2, color='r')


    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'blue'
    ax2.set_ylabel('$\\theta$=K0L [rad]', color=color)  # we already handled the x-label with ax1
    ax2.tick_params(axis='y', labelcolor=color)
    if ylim2 is not None:
        plt.ylim(ylim2[0], ylim2[1])
    else:
        plt.ylim(-.3,.3)
    #plt.ylim(-.3,.3)

    for quad in quads_table.name:
        k0l = transfer_line.get_strengths().rows[quad].k0l[0] 
        aux = tw1.rows[quad].s[0]
        #print(quad, k0l) #transfer_line.get(quad)
        try:
            length = transfer_line.get(quad).length
        except:
            length=0
        plotLatticeSeries(plt.gca(),aux, length, height=k0l, v_offset=k0l/2, color='b')

    ax3 = plt.subplot2grid((3,3), (1,0), colspan=3, rowspan=2,sharex=ax1)

    plt.plot(tw1['s'], tw1['betx'], label= r'$\beta_x$', c="blue")
    plt.plot(tw1['s'], tw1['bety'], label=r'$\beta_y$', c="red")
    plt.legend()
    plt.grid()
    plt.ylabel("[m]")
    plt.xlabel("s [m]")

    ax4 = plt.gca().twinx()
    plt.plot(tw1['s'], tw1["dx"], c="brown", lw=5)
    plt.ylabel(r"$D_x$ [m]", c="brown")
    plt.tick_params(axis='y', labelcolor='brown')
    if ylim3 is not None:
        plt.ylim(ylim3[0], ylim3[1])
    else:
        plt.ylim(-5, 20)
    return fig, ax1, ax2, ax3, ax4;

fig, ax1, ax2, ax3, ax4 = useful_plots(line, mytwiss, filter_elements="Multipole")
# %%
mySurvey = line.survey()
mySurvey = mySurvey.rows[r'^(mq|mb).*']

qfSurvey=mySurvey.rows[r'mqf.*']
qdSurvey=mySurvey.rows[r'mqd.*']
mbSurvey=mySurvey.rows[r'mb.*']



fig, ax = plt.subplots(figsize=(9, 6))
plt.plot(qfSurvey.X,qfSurvey.Z,'ob')
plt.plot(qdSurvey.X,qdSurvey.Z,'or')
plt.plot(mbSurvey.X,mbSurvey.Z,'.k')
plt.axis('square')
plt.xlabel('X [m]')
plt.ylabel('Z [m]')
plt.grid()




# %%
#### include dispersion suppressor and straight section


pc_GeV = 20.0

circum = 2000.0 # circumference
ncell = 40 # number of cells
lcell = circum/ncell # length of cell
lq=3.0 # length of quadrupole
#number_dipoles_percell = 4
nnorm=128.
theta = 2.0*np.pi/(nnorm) #(2.0*np.pi)/ncell/number_dipoles_percell
k1 = 0.0098 # quadrupole strength
lsex = 0.00001
ksf = +0.017041/ncell
ksd = -0.024714/ncell

env = xt.Environment()

env.vars({'lcell': lcell, 
          'lq': lq,
          'theta': theta,
          'kf': k1,
          'kd': -k1,
          'kfl': k1*lq,
          'kdl': -k1*lq,
          'lsex': lsex,
          'ksf': ksf,
            'ksd': ksd,
          })

#env.new('mb', xt.Bend, k0='theta', h='theta')
env.new('mb', xt.Multipole, knl=['theta', 0, 0], hxl='theta')
env.new('mqf', xt.Multipole, knl=[0, "kfl", 0])
env.new('mqd', xt.Multipole, knl=[0, "kdl", 0])
env.new("msf", xt.Multipole, knl=[0, 0, "ksf"])
env.new("msd", xt.Multipole, knl=[0, 0, "ksd"])


cell = env.new_line(components=[
    env.new('cell_marker_start', xt.Marker, at=0),
    env.place('mqf', at=0),
    env.place('msf', at=lsex*0.5),
    env.place('mb', at=0.15*lcell),
    env.place('mb', at=0.35*lcell),
    env.place("mqd", at=0.5*lcell),
    env.place('msd', at=0.5*lcell + lsex*0.5),
    env.place('mb', at=0.65*lcell),
    env.place('mb', at=0.85*lcell),
    env.new('cell_marker_end', xt.Marker, at=lcell),
])


cell.to_pandas()

#%%
dispersion_suppressor = env.new_line(components=[
    env.new('DS_marker_start', xt.Marker, at=0),
    env.place('mqf', at=0),
    env.place("mqd", at=0.5*lcell),
    env.place('mqf', at=1.0*lcell),
    env.place('mb', at=1.0*lcell + 0.15*lcell),
    env.place('mb', at=1.0*lcell + 0.35*lcell),
    env.place("mqd", at=lcell + 0.5*lcell),
    env.place('mb', at=1.0*lcell + 0.65*lcell),
    env.place('mb', at=1.0*lcell + 0.85*lcell),
    env.new('DS_marker_end', xt.Marker, at=2.0*lcell),
])

dispersion_suppressor.to_pandas()



#%%
# straight section
straight_section = env.new_line(components=[
    env.new('SS_marker_start', xt.Marker, at=0),
    env.place('mqf', at=0),
    env.place("mqd", at=0.5*lcell),
    env.place('mqf', at=1.0*lcell),
    env.place("mqd", at=1.0*lcell + 0.5*lcell),
    env.new('SS_marker_end', xt.Marker, at=2.0*lcell),
])

straight_section.to_pandas()

#%%

# dispersion suppressor reversed

dispersion_suppressor2 = env.new_line(components=[
    env.new('DS2_marker_start', xt.Marker, at=0),
    env.place('mqf', at=0),
    env.place('mb', at=0.15*lcell),
    env.place('mb', at=0.35*lcell),
    env.place("mqd", at=0.5*lcell),
    env.place('mb', at= 0.65*lcell),
    env.place('mb', at=0.85*lcell),
    env.place('mqf', at=1.0*lcell),
    env.place("mqd", at=1.0*lcell + 0.5*lcell),
    env.new('DS2_marker_end', xt.Marker, at=2.0*lcell),
])

dispersion_suppressor2.to_pandas()

#%%


#%% append in cells number_of_FODO times cell
line = env.new_line(components=
                    
                    [env.place(cell)]*4
                    + [env.place(dispersion_suppressor)]*1
                    + [env.new('SS_marker_start_first', xt.Marker)]
                    + [env.place(straight_section)]*1
                    + [env.place(dispersion_suppressor2)]*1
                    + [env.place(cell)]*14
                    + [env.place(dispersion_suppressor)]*1
                    + [env.place(straight_section)]*1
                    + [env.place(dispersion_suppressor2)]*1
                    + [env.place(cell)]*10
                    
                    )

line.to_pandas()
# %%

line.particle_ref = xt.Particles(p0c=pc_GeV*1e9, #eV
                                 q0=1, mass0=xt.PROTON_MASS_EV)
context = xo.ContextCpu()
line.build_tracker(_context=context)
line.twiss(method="4d")

mytwiss = line.twiss(method="4d")
fig, ax1, ax2, ax3, ax4 = useful_plots(line, mytwiss, filter_elements="Multipole")

#%%
opt = line.match(
    solve=False,
    method='4d',
    vary=xt.VaryList(['kfl', 'kdl'], step=1e-5),
    targets=xt.TargetSet(qx=ncell/6., qy=ncell/6., tol=1e-6, tag='tune'
    ))
#%%
print('Before match:')
opt.target_status()

opt.solve()

print('After match:')
opt.target_status()

print('\nMatch history')
opt.log()

# %%
knobs_after_match = opt.get_knob_values()
knobs_before_match = opt.get_knob_values(iteration=0)
print(knobs_before_match)


#%%
mytwiss = line.twiss(method="4d")
fig, ax1, ax2, ax3, ax4 = useful_plots(line, mytwiss, filter_elements="Multipole")
# %%
mySurvey = line.survey()
mySurvey = mySurvey.rows[r'^(mq|mb).*']

qfSurvey=mySurvey.rows[r'mqf.*']
qdSurvey=mySurvey.rows[r'mqd.*']
mbSurvey=mySurvey.rows[r'mb.*']



fig, ax = plt.subplots(figsize=(9, 6))
plt.plot(qfSurvey.X,qfSurvey.Z,'ob')
plt.plot(qdSurvey.X,qdSurvey.Z,'or')
plt.plot(mbSurvey.X,mbSurvey.Z,'.k')
plt.axis('square')
plt.xlabel('X [m]')
plt.ylabel('Z [m]')
plt.grid()
# %%
line_cycled = line.cycle("SS_marker_start_first")
# %%
mySurvey = line_cycled.survey()
mySurvey = mySurvey.rows[r'^(mq|mb).*']

qfSurvey=mySurvey.rows[r'mqf.*']
qdSurvey=mySurvey.rows[r'mqd.*']
mbSurvey=mySurvey.rows[r'mb.*']

fig, ax = plt.subplots(figsize=(9, 6))
plt.plot(qfSurvey.X,qfSurvey.Z,'ob')
plt.plot(qdSurvey.X,qdSurvey.Z,'or')
plt.plot(mbSurvey.X,mbSurvey.Z,'.k')
plt.axis('square')
plt.xlabel('X [m]')
plt.ylabel('Z [m]')
plt.grid()
# %%

# Half dipole approach



pc_GeV = 20.0

circum = 2000.0 # circumference
ncell = 40 # number of cells
lcell = circum/ncell # length of cell
lq=3.0 # length of quadrupole
#number_dipoles_percell = 4
nnorm=120.0
theta = 2.0*np.pi/(nnorm)
theta2 = 1.0*np.pi/(nnorm)  #(2.0*np.pi)/ncell/number_dipoles_percell
k1 = 0.0098 # quadrupole strength
lsex = 0.00001
ksf = +0.017041/20.0
ksd = -0.024714/20.0

env = xt.Environment()

env.vars({'lcell': lcell, 
          'lq': lq,
          'theta': theta,
          'theta2': theta2,
          'kf': k1,
          'kd': -k1,
          'kfl': k1*lq,
          'kdl': -k1*lq,
          'lsex': lsex,
          'ksf': ksf,
            'ksd': ksd,
          })

#env.new('mb', xt.Bend, k0='theta', h='theta')
env.new('mb', xt.Multipole, knl=['theta', 0, 0], hxl='theta')
env.new('mb2', xt.Multipole, knl=['theta2', 0, 0], hxl='theta2')
env.new('mqf', xt.Multipole, knl=[0, "kfl", 0])
env.new('mqd', xt.Multipole, knl=[0, "kdl", 0])
env.new("msf", xt.Multipole, knl=[0, 0, "ksf"])
env.new("msd", xt.Multipole, knl=[0, 0, "ksd"])


cell = env.new_line(components=[
    env.new('cell_marker_start', xt.Marker, at=0),
    env.place('mqf', at=0),
    env.place('msf', at=lsex*0.5),
    env.place('mb', at=0.15*lcell),
    env.place('mb', at=0.35*lcell),
    env.place("mqd", at=0.5*lcell),
    env.place('msd', at=0.5*lcell + lsex*0.5),
    env.place('mb', at=0.65*lcell),
    env.place('mb', at=0.85*lcell),
    env.new('cell_marker_end', xt.Marker, at=lcell),
])


cell.to_pandas()

#%%
dispersion_suppressor = env.new_line(components=[
    env.new('DS_marker_start', xt.Marker, at=0),
    env.place('mqf', at=0),
    env.place('mb2', at=0.15*lcell),
    env.place('mb2', at=0.35*lcell),
    env.place("mqd", at= 0.5*lcell),
    env.place('mb2', at= 0.65*lcell),
    env.place('mb2', at=0.85*lcell),
    env.new('DS_marker_end', xt.Marker, at=1.0*lcell),
])

dispersion_suppressor.to_pandas()



#%%
# straight section
straight_section = env.new_line(components=[
    env.new('SS_marker_start', xt.Marker, at=0),
    env.place('mqf', at=0),
    env.place("mqd", at=0.5*lcell),
    env.place('mqf', at=1.0*lcell),
    env.place("mqd", at=1.0*lcell + 0.5*lcell),
    env.new('SS_marker_end', xt.Marker, at=2.0*lcell),
])

straight_section.to_pandas()

#%%

# dispersion suppressor reversed

dispersion_suppressor2 = env.new_line(components=[
    env.new('DS2_marker_start', xt.Marker, at=0),
    env.place('mqf', at=0),
    env.place('mb2', at=0.15*lcell),
    env.place('mb2', at=0.35*lcell),
    env.place("mqd", at=0.5*lcell),
    env.place('mb2', at= 0.65*lcell),
    env.place('mb2', at=0.85*lcell),
    env.new('DS2_marker_end', xt.Marker, at=1.0*lcell),
])

dispersion_suppressor2.to_pandas()

#%%


#%% append in cells number_of_FODO times cell
line = env.new_line(components=
                    
                    [env.place(cell)]*3
                    + [env.place(dispersion_suppressor)]*3
                    + [env.new('SS_marker_start_first', xt.Marker)]
                    + [env.place(straight_section)]*1
                    + [env.place(dispersion_suppressor2)]*3
                    + [env.place(cell)]*12
                    + [env.place(dispersion_suppressor)]*3
                    + [env.place(straight_section)]*1
                    + [env.place(dispersion_suppressor2)]*3
                    + [env.place(cell)]*9
                    
                    )

line.to_pandas()
# %%

line.particle_ref = xt.Particles(p0c=pc_GeV*1e9, #eV
                                 q0=1, mass0=xt.PROTON_MASS_EV)
context = xo.ContextCpu()
line.build_tracker(_context=context)
line.twiss(method="4d")

mytwiss = line.twiss(method="4d")
fig, ax1, ax2, ax3, ax4 = useful_plots(line, mytwiss, filter_elements="Multipole")

#%%
opt = line.match(
    solve=False,
    method='4d',
    vary=xt.VaryList(['kfl', 'kdl'], step=1e-5),
    targets=xt.TargetSet(qx=6.7, qy=6.65, tol=1e-6, tag='tune'
    ))
#%%
print('Before match:')
opt.target_status()

opt.solve()

print('After match:')
opt.target_status()

print('\nMatch history')
opt.log()

# %%
knobs_after_match = opt.get_knob_values()
knobs_before_match = opt.get_knob_values(iteration=0)
print(knobs_before_match)


#%%
mytwiss = line.twiss(method="4d")
fig, ax1, ax2, ax3, ax4 = useful_plots(line, mytwiss, filter_elements="Multipole")
# %%
mySurvey = line.survey()
mySurvey = mySurvey.rows[r'^(mq|mb).*']

qfSurvey=mySurvey.rows[r'mqf.*']
qdSurvey=mySurvey.rows[r'mqd.*']
mbSurvey=mySurvey.rows[r'mb.*']



fig, ax = plt.subplots(figsize=(9, 6))
plt.plot(qfSurvey.X,qfSurvey.Z,'ob')
plt.plot(qdSurvey.X,qdSurvey.Z,'or')
plt.plot(mbSurvey.X,mbSurvey.Z,'.k')
plt.axis('square')
plt.xlabel('X [m]')
plt.ylabel('Z [m]')
plt.grid()
# %%
