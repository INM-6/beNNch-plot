import benchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


args = {
    'data_hash': '9acabf83-e1e1-4da4-a086-79138536c9b2',
    'data_path': './timing_results',
    'catalogue_path': 'catalogue.yaml',
    'manually_set_plot_name': 'MAM node scaling',
    'x_axis': ['num_nodes'],
    'time_scaling': 1e3
}
# args = {
#     'data_hash': 'fda5d63a-5648-4a0d-b180-f3633b33cbcf',
#     'data_path': './timing_results',
#     'catalogue_path': 'catalogue.yaml',
#     'manually_set_plot_name': 'MAM node scaling',
#     'x_axis': ['num_nodes'],
#     'time_scaling': 1e3
# }


# Instantiate class
B = bp.BenchPlot(**args)

# Plotting
widths = [1, 1]
heights = [3, 1]
fig = plt.figure(figsize=(12, 6), constrained_layout=True)
spec = gridspec.GridSpec(ncols=2, nrows=2, figure=fig, width_ratios=widths,
                         height_ratios=heights)

ax1 = fig.add_subplot(spec[:, 0])
ax2 = fig.add_subplot(spec[0, 1])
ax3 = fig.add_subplot(spec[1, 1])


B.plot_fractions(axis=ax1,
                 fill_variables=['wall_time_creation+wall_time_connect',
                                 'wall_time_sim'],
                 interpolate=True,
                 step=None)
B.plot_main(quantities=['sim_factor'], axis=ax2)
B.plot_fractions(axis=ax2,
                 fill_variables=[
                     'phase_communicate_factor',
                     'phase_update_factor',
                     'phase_deliver_factor',
                 ],
                 )

B.plot_fractions(axis=ax3,
                 fill_variables=[
                     'frac_phase_communicate',
                     'frac_phase_update',
                     'frac_phase_deliver',
                 ],
                 )

ax1.set_xlabel('Number of Nodes')
ax1.set_ylabel('wall time ' + r'$T_{\mathrm{wall}}$' + ' [s]')
ax2.set_ylabel(r'real-time factor $T_{\mathrm{wall}}$' + ' / ' +
               r'$T_{\mathrm{model}}$')
ax3.set_xlabel('Number of Nodes')

# ax2.set_ylim((30,180))

ax1.set_title('A', loc='left', fontsize=16, fontweight="bold")
ax2.set_title('B', loc='left', fontsize=16, fontweight="bold")
ax3.set_title('C', loc='left', fontsize=16, fontweight="bold")

ax1.legend()
ax2.legend()
# B.merge_legends(ax2, ax3)
plt.savefig('golosio_jureca.pdf')
