# %%
from typing import OrderedDict
import numpy as np
import xtrack as xt

number_of_arcs = 8
number_of_cells_per_arc = 4
dipoles_per_cell = 2
number_of_dipoles = number_of_arcs * number_of_cells_per_arc * dipoles_per_cell

lbend = 0.3
my_k0 = np.pi*2/number_of_dipoles/lbend
# Define the lattice of a single cell
cell = OrderedDict({
    'mqf': xt.Quadrupole(length=0.3, k1=0.01),
    'drift_1':  xt.Drift(length=0.4),
    'mb1': xt.Bend(length=lbend, k0=my_k0, h=my_k0),
    'drift_2':  xt.Drift(length=0.4), 
    'mqd': xt.Quadrupole(length=0.3, k1=-0.01),
    'drift_3':  xt.Drift(length=0.4),
    'mb2': xt.Bend(length=lbend, k0=my_k0, h=my_k0),
    'drift_4':  xt.Drift(length=0.4),})

def get_cell(cell, cell_number, arc_number):
    # take the cell and add to the keys the cell number and arc number
    cell_ = {}
    for key, value in cell.items():
        cell_[f'{key}_{cell_number}_{arc_number}'] = value
    return cell_

# concatenate a list a of dictionaries
my_list = [get_cell(cell, cell_number, arc_number) for arc_number in range(1, number_of_arcs+1) for cell_number in range(1, number_of_cells_per_arc+1)]

# defines element as the dictionary resulting from the concatenation of my_list
elements = {k: v for d in my_list for k, v in d.items()}



# Build the ring
line = xt.Line(elements=elements,
               element_names=elements.keys(),
)
# Define reference particle
line.particle_ref = xt.Particles()


tw = line.twiss4d()
# %%
import xplt
# %%
plot = xplt.FloorPlot(line=line)


plot = xplt.TwissPlot(tw, line=line)
# %%
