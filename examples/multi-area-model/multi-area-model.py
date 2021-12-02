import numpy as np
import benchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


args = {
    'data_file': '45011f6d-c3c2-4f2c-b884-af04e9edc5b9.csv',
    'x_axis': ['num_nodes'],
    'time_scaling': 1e3
}


# Instantiate class
B = bp.BenchPlot(**args)

# Plotting
widths = [1, 1]
heights = [3, 1]
fig = plt.figure(figsize=(12, 6), constrained_layout=True)
spec = gridspec.GridSpec(ncols=2, nrows=2, figure=fig,
                         width_ratios=widths, height_ratios=heights)

ax1 = fig.add_subplot(spec[:, 0])
ax2 = fig.add_subplot(spec[0, 1])
ax3 = fig.add_subplot(spec[1, 1])


B.plot_fractions(axis=ax1,
                 fill_variables=['wall_time_create+wall_time_connect',
                                 'wall_time_sim'],
                 interpolate=True,
                 step=None,
                 error=True)
B.plot_main(quantities=['sim_factor'], axis=ax2, error=True)
B.plot_fractions(axis=ax2,
                 fill_variables=[
                     'phase_update_factor',
                     'phase_collocate_factor',
                     'phase_communicate_factor',
                     'phase_deliver_factor'
                 ])
B.plot_fractions(axis=ax3,
                 fill_variables=[
                     'frac_phase_communicate',
                     'frac_phase_update',
                     'frac_phase_deliver'])

ax2.set_ylim(0,300)
B.simple_axis(ax1)
B.simple_axis(ax2)

ax1.set_xlabel('Number of nodes')
ax1.set_ylabel(r'$T_{\mathrm{wall}}$ [s] for $T_{\mathrm{model}} =$'
               + f'{np.unique(B.df.model_time_sim.values)[0]} s')
ax2.set_ylabel(r'real-time factor $T_{\mathrm{wall}}/$'
               r'$T_{\mathrm{model}}$')
ax3.set_xlabel('Number of nodes')
ax3.set_ylabel(r'relative $T_{\mathrm{wall}}$ [%]')

ax1.legend()
ax2.legend()

plt.savefig('scaling.pdf')
