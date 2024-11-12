#%%
import xtrack as xt
import numpy as np
import matplotlib.pyplot as plt
import xobjects as xo
import matplotlib.patches as patches

#%%
quadrupoleLength=0.1
cellLength=10
myk1 = 0.1
myk2 = 0.1
myk3 = 0.1
myk4 = 0.1
theta1 = 0
theta2 = 0
slice_sequence = True
if slice_sequence:
    n_slices_quads = 5
    n_slices_drifts = 10
else:
    n_slices_quads = 1
    n_slices_drifts = 1

env = xt.Environment()
env.vars({'ql': quadrupoleLength,
            'cellLength': cellLength,
            'myk1': myk1,
            'myk2': myk2,
            'myk3': myk3,
            'myk4': myk4,
            'theta1': theta1,
            'theta2': theta2})
#%%
env.new('q1', xt.Quadrupole, length='ql', k1='myk1')
env.new('q2', xt.Quadrupole, length='ql', k1='myk2')
env.new('q3', xt.Quadrupole, length='ql', k1='myk3')
env.new('q4', xt.Quadrupole, length='ql', k1='myk4')
env.new('final_drift', xt.Drift, length=1)
env.new("hkicker1", xt.Multipole, knl=["theta1", 0, 0])
env.new("hkicker2", xt.Multipole, knl=["theta2", 0, 0])

transfer_line = env.new_line(components=[
env.place('q1', at=2),
env.place("hkicker1", at=2.4),
env.place('q2', at=4),
env.place('q3', at=6),
env.place("hkicker2", at=6.4),
env.place('q4', at=8),
env.place('final_drift', at=9.5)
])


transfer_line.particle_ref = xt.Particles(p0c=2e9, #eV
                                 q0=1, mass0=xt.PROTON_MASS_EV)
context = xo.ContextCpu()

if slice_sequence:
    transfer_line.slice_thick_elements(
        slicing_strategies=[
            # Slicing with thin elements
            xt.Strategy(slicing=xt.Uniform(n_slices_drifts), element_type=xt.Drift), 
            xt.Strategy(slicing=xt.Uniform(n_slices_quads), element_type=xt.Quadrupole), 
        ])
    
    filter_elements="ThinSliceQuadrupole"
else:
    filter_elements="Quadrupole"

transfer_line.build_tracker(_context=context)
transfer_line.to_pandas()

#%%
transfer_line.get_table().rows["q.*"]

#%%
try:
    transfer_line.twiss(method='4d')
except:
    print("No periodic solution found!")
# %%
tw1 = transfer_line.twiss(betx=1, bety=2)
# %%
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
        k1l = transfer_line.get_strengths().rows[quad].k1l[0] * n_slices_quads
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
        k0l = transfer_line.get_strengths().rows[quad].k0l[0] * n_slices_quads
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
    plt.plot(tw1['s'], tw1["dx"], c="brown")
    plt.ylabel(r"$D_x$ [m]", c="brown")
    plt.tick_params(axis='y', labelcolor='brown')
    if ylim3 is not None:
        plt.ylim(ylim3[0], ylim3[1])
    else:
        plt.ylim(-5, 150)
    return fig, ax1, ax2, ax3, ax4;

fig, ax1, ax2, ax3, ax4 = useful_plots(transfer_line, tw1, filter_elements=filter_elements)
# %%

print("betx end: ", tw1.rows["_end.*"]["betx"][0])
print("bety end: ", tw1.rows["_end.*"]["bety"][0])
print("alphax end: ", tw1.rows["_end.*"]["alfx"][0])
print("alphay end: ", tw1.rows["_end.*"]["alfy"][0])
initial_end_betx = tw1.rows["_end.*"]["betx"][0]
initial_end_bety = tw1.rows["_end.*"]["bety"][0]
initial_end_alfx = tw1.rows["_end.*"]["alfx"][0]
initial_end_alfy = tw1.rows["_end.*"]["alfy"][0]


# %%
transfer_line.vars.get_table()

#%%
opt = transfer_line.match(
    start=tw1.name[0],
    end=tw1.name[-1],
    betx=1, bety=2,
    solve=False,
    method='4d',
    vary=xt.VaryList(['myk1', 'myk2', 'myk3', 'myk4'], step=1e-5),
    targets=xt.TargetSet(
        betx=2,
        bety=1,
        alfx=0,
        alfy=0,
        at=xt.END
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
print(knobs_after_match)
# %%
tw_after_matching = transfer_line.twiss(betx=1, bety=2)
print(tw_after_matching["betx"][0], tw_after_matching["bety"][0], tw_after_matching["alfx"][0], tw_after_matching["alfy"][0])
print(tw_after_matching["betx"][-1], tw_after_matching["bety"][-1], tw_after_matching["alfx"][-1], tw_after_matching["alfy"][-1])

# %%
fig, ax1, ax2, ax3, ax4 = useful_plots(transfer_line, tw_after_matching, ylim1=(-2,2), ylim2=(-.3,.3), ylim3=(-5, 150), filter_elements=filter_elements)
# %%

opt = transfer_line.match(
    start=tw1.name[0],
    end=tw1.name[-1],
    betx=1, bety=2,
    solve=True,
    method='4d',
    n_steps_max=500,
    vary=xt.VaryList(['myk1', 'myk2', 'myk3', 'myk4'], step=1e-5),
    targets=xt.TargetSet(
        betx=initial_end_betx,
        bety=initial_end_bety,
        alfx=initial_end_alfx,
        alfy=initial_end_alfy,
        at=xt.END
    ))

tw_after_matching2 = transfer_line.twiss(betx=1, bety=2)
fig, ax1, ax2, ax3, ax4 = useful_plots(transfer_line, tw_after_matching2, ylim1=(-2,2), ylim2=(-.3,.3), ylim3=(-5, 150), filter_elements=filter_elements)
plt.sca(ax3)
plt.plot(tw1.s, tw1.betx, label="Initial", c="b", linestyle='--')
plt.plot(tw1.s, tw1.bety, label="Initial", c="r", linestyle='--')

#%%


print(tw_after_matching2["betx"][0], tw_after_matching2["bety"][0], tw_after_matching2["alfx"][0], tw_after_matching2["alfy"][0])
print(tw_after_matching2["betx"][-1], tw_after_matching2["bety"][-1], tw_after_matching2["alfx"][-1], tw_after_matching2["alfy"][-1])

# %%
transfer_line.vars["myk1"]._info()


# %%
transfer_line.vars["myk1"] = 0.05
transfer_line.vars["myk2"] = 0.05
transfer_line.vars["myk3"] = 0.05
transfer_line.vars["myk4"] = 0.05


opt = transfer_line.match(
    start=tw1.name[0],
    end=tw1.name[-1],
    betx=1, bety=2,
    solve=True,
    method='4d',
    n_steps_max=500,
    vary=xt.VaryList(['myk1', 'myk2', 'myk3', 'myk4'], step=1e-5),
    targets=xt.TargetSet(
        betx=initial_end_betx,
        bety=initial_end_bety,
        alfx=initial_end_alfx,
        alfy=initial_end_alfy,
        at=xt.END
    ))

tw_after_matching3 = transfer_line.twiss(betx=1, bety=2)
fig, ax1, ax2, ax3, ax4 = useful_plots(transfer_line, tw_after_matching3, ylim1=(-0.05,0.05), ylim2=(-.3,.3), ylim3=(-5, 150), filter_elements=filter_elements)
plt.sca(ax3)
plt.plot(tw1.s, tw1.betx, label="Initial", c="b", linestyle='--')
plt.plot(tw1.s, tw1.bety, label="Initial", c="r", linestyle='--')


# %%
# Matrix response of the kickers
transfer_line.vars["theta1"] = 1e-6
transfer_line.vars["theta2"] = 0e-6

tw_kicker = transfer_line.twiss(betx=1, bety=2)
m11 = tw_kicker.x[-1]/1e-6
m21 = tw_kicker.px[-1]/1e-6
print(m11, m21)

transfer_line.vars["theta1"] = 0e-6
transfer_line.vars["theta2"] = 1e-6

tw_kicker = transfer_line.twiss(betx=1, bety=2)
m12 = tw_kicker.x[-1]/1e-6
m22 = tw_kicker.px[-1]/1e-6
print(m12, m22)

# %%
M_response=np.array([[m11, m12], [m21, m22]])
M_response
# %%

mySolution=np.linalg.inv(M_response)@np.array([[1e-3],[0]])
mySolution
# %%

transfer_line.vars["theta1"] = mySolution[0][0]
transfer_line.vars["theta2"] = mySolution[1][0]

aux= transfer_line.twiss(betx=1, bety=2)
aux["x"], aux["px"]

# %%
plt.plot(aux['s'],aux['x']*1000,'b.-',label='x [mm]')
plt.plot(aux['s'],aux['px']*1000,'r.-',label='px [mrad]')
plt.grid()
plt.xlabel('s [m]')
plt.legend(loc='best')
# %%
