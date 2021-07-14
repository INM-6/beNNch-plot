import benchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


args = {
    'data_hash': '0d1424b7-bd4c-4134-8494-624f34aaf0b6',
    'data_path': './timing_results',
    'catalogue_path': 'catalogue.yaml',
    'manually_set_plot_name': 'MAM omp vs mpi',
    'x_axis': ['num_omp_threads'],
    'time_scaling': 1e3
}
# args = {
#     'data_hash': '9b68869d-fa1c-4cee-b16f-45b3951c059e',
#     'data_path': './timing_results',
#     'catalogue_path': 'catalogue.yaml',
#     'manually_set_plot_name': 'MAM omp vs mpi',
#     'x_axis': ['num_omp_threads'],
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
                 fill_variables=['wall_time_sim',
                                 'wall_time_creation+wall_time_connect'],
                 interpolate=True,
                 step=None)
B.plot_main(quantities=['sim_factor', 'phase_total_factor'], axis=ax2)
B.plot_fractions(axis=ax3,
                 fill_variables=[
                     'frac_phase_communicate',
                     'frac_phase_update',
                     'frac_phase_deliver'])

ax1.set_xlabel('# threads per node')
ax1.set_ylabel('wall time [s]')
ax2.set_ylabel(r'real-time factor $T_{\mathrm{wall}}$'
               r'$T_{\mathrm{model}}$')
ax3.set_xlabel('# threads per node')

# ax2.set_ylim((30,180))

ax1.legend()
# B.merge_legends(ax2, ax3)

plt.savefig('omp_mpi_JUSUF_64.pdf')
