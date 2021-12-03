"""
benchplot - standardized plotting routines for performance benchmarks.
Copyright (C) 2021 Forschungszentrum Juelich GmbH, INM-6

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.

SPDX-License-Identifier: GPL-3.0-or-later
"""
import numpy as np
import benchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


"""
define what to plot:
- data_file:
    Path to .csv file containing benchmarking measurements.
- x_axis:
    Giving a list of strings corresponding to the main scaling
    variable, typically 'num_nodes' or 'num_nvp'.
- time_scaling:
    Quotient between unit time of timing measurement and
    simulation. Usually, the former is given in s while
    the latter is given in ms. 
"""
args = {
    'data_file': '8d196bc5-b5f5-448b-8571-bf695ed64d4a.csv',
    'x_axis': ['num_nvp'],
    'time_scaling': 1e3
}

# Figure layout
B = bp.BenchPlot(**args)

# Plotting
widths = [1]
heights = [3, 1]
fig = plt.figure(figsize=(6, 6), constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=2, figure=fig, width_ratios=widths,
                         height_ratios=heights)

ax1 = fig.add_subplot(spec[0, :])
ax2 = fig.add_subplot(spec[1, :])

# Add plots
B.plot_main(quantities=['sim_factor'], axis=ax1, log=(False, True))
B.plot_fractions(axis=ax2,
                 fill_variables=[
                     'frac_phase_communicate',
                     'frac_phase_update',
                     'frac_phase_deliver',
                     'frac_phase_collocate'
                 ],
                 )

# Set labels, limits etc.
ax1.set_ylabel(r'$T_{\mathrm{wall}}$ [s] for $T_{\mathrm{model}} =$'
               + f'{np.unique(B.df.model_time_sim.values)[0]} s')
ax1.set_xlabel('Number of virtual processes')
ax2.set_ylabel(r'relative $T_{\mathrm{wall}}$ [%]')
B.merge_legends(ax1, ax2)

# Save figure
plt.savefig('scaling.pdf')
