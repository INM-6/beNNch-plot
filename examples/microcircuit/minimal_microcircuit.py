import benchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


args = {
    'data_hash': '1c801424-90d9-447d-91e9-a9839a2f6b2f',
    'data_path': '../timing_results',
    'catalogue_path': 'catalogue_microcircuit_jusuf.yaml',
    'manually_set_plot_name': 'Microcircuit',
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

ax1.set_ylabel(r'real-time factor $T_{\mathrm{wall}}/$'
               r'$T_{\mathrm{model}}$')
ax1.set_xlabel('number of vps')
ax1.legend()
ax2.set_ylabel(r'relative wall time $[\%]$')
B.merge_legends(ax1, ax2)

plt.savefig('../plots/microcircuit_jusuf.pdf')
