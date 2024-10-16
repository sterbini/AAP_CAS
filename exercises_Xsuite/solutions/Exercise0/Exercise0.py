#%%
# This is a simple example on how to use Mad-X in Python to match a 10 m long FODO lattice. Each quadrupole is 1.5 m long.

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xtrack as xt
import xobjects as xo

#%%
env = xt.Environment()

#%%
env.vars({ 'kf': 0.2985, 
            'kd': -0.2985,
            'lquad': 0.5, 
            'ldrift': 4.5})

env.new('mq', xt.Quadrupole, length=env["lquad"])
env.new('mq.f', 'mq', k1='kf')
env.new('mq.d', 'mq', k1='kd')

#%%
fodo = env.new_line(components = [
                    env.place('mq.f', at=4.5 + env["lquad"]/2),
                    env.place('mq.d', at=9.5 + env["lquad"]/2),               
                    ]
                    )
fodo.to_pandas()
# %%
# 2. Definition of the beam
fodo.particle_ref = xt.Particles(p0c=6500e9, #eV
                                 q0=1, mass0=xt.PROTON_MASS_EV)
# %%
context = xo.ContextCpu()
fodo.build_tracker(_context=context)
# %%
tw = fodo.twiss(method='4d')
# %%
fig, ax = plt.subplots(figsize=(9, 6))
plt.plot(tw.s, tw.betx, 'o-', label=r"$\beta_x$", c="b", )
plt.plot(tw.s, tw.bety, 'o-',label=r"$\beta_y$", c="r")
plt.grid()
plt.ylabel("[m]")
plt.xlabel("s [m]")
plt.legend()

#%%
fodo.twiss4d().plot()

#%%
fodo.vars.get_table()

#%%

opt = fodo.match(
    solve=False,
    method='4d',
    vary=xt.VaryList(['kf', 'kd'], step=1e-5),
    targets=xt.TargetSet(
        qx=0.25,
        qy=0.25,
    ))

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
tw_after_matching = fodo.twiss(method='4d')
# %%
fig, ax = plt.subplots(figsize=(9, 6))
plt.plot(tw.s, tw.betx, 'o-', label=r"$\beta_x$ before", c="b", )
plt.plot(tw.s, tw.bety, 'o-',label=r"$\beta_y$ before", c="r")

plt.plot(tw_after_matching.s, tw_after_matching.betx, 'o--', label=r"$\beta_x$ after", c="b", )
plt.plot(tw_after_matching.s, tw_after_matching.bety, 'o--',label=r"$\beta_y$ after", c="r")
plt.grid()
plt.ylabel("[m]")
plt.xlabel("s [m]")
plt.legend()

# %%
tunes_deg = np.arange(20, 160, 10)
tunes = tunes_deg/360

results_kf = []
results_kd = []
for current_tune in tunes:
    opt = fodo.match(
    solve=True,
    method='4d',
    vary=xt.VaryList(['kf', 'kd'], step=1e-5),
    targets=xt.TargetSet(
        qx=current_tune,
        qy=current_tune,
    ))
    knobs_after_match = opt.get_knob_values()
    results_kf.append(knobs_after_match['kf'])
    results_kd.append(knobs_after_match['kd'])
    
    
# %%
f = 1.0/np.array(results_kf)/fodo['mq.f'].length
analytical = np.arcsin(10/(4*f))/np.pi

fig, ax = plt.subplots(figsize=(9, 6))
plt.plot(np.array(results_kf)*fodo['mq.f'].length, tunes, 'o-',  c="b", label="XSuite")
plt.plot(np.array(results_kf)*fodo['mq.f'].length, analytical, 'o-',  c="r", label="thin lens approximation")
plt.grid()
plt.ylabel('Q1')
plt.xlabel('K1L [m$^{-1}$]')
plt.legend()
# %%
