import numpy as np
import benchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


args = {
    'data_file': '8d196bc5-b5f5-448b-8571-bf695ed64d4a.csv',
    'x_axis': ['num_nvp'],
    'time_scaling': 1e3
}

# Instantiate class
B = bp.BenchPlot(**args)

# Plotting
widths = [1]
heights = [3, 1]
fig = plt.figure(figsize=(6, 6), constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=2, figure=fig, width_ratios=widths,
                         height_ratios=heights)

ax1 = fig.add_subplot(spec[0, :])
ax2 = fig.add_subplot(spec[1, :])


B.plot_main(quantities=['sim_factor'], axis=ax1, log=(False, True))
B.plot_fractions(axis=ax2,
                 fill_variables=[
                     'frac_phase_communicate',
                     'frac_phase_update',
                     'frac_phase_deliver',
                     'frac_phase_collocate'
                 ],
                 )

ax1.set_ylabel(r'$T_{\mathrm{wall}}$ [s] for $T_{\mathrm{model}} =$'
               + f'{np.unique(B.df.model_time_sim.values)[0]} s')
ax1.set_xlabel('Number of virtual processes')
ax2.set_ylabel(r'relative $T_{\mathrm{wall}}$ [%]')
B.merge_legends(ax1, ax2)

plt.savefig('scaling.pdf')
