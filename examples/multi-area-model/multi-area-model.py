import benchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


args = {
    'data_hash': '27B3A1AC-0145-46EA-8CBE-786F4D920807',
    'data_path': './',
    'catalogue_path': 'catalogue.yaml',
    'save_path': './',
    'manually_set_plot_name': 'MAM node scaling',
    'x_axis': ['num_nodes'],
    'y_axis': [['wall_time_sim',
                'wall_time_creation+wall_time_connect'],
               ['sim_factor', 'phase_total_factor']],
    'x_label': ['Nodes'],
    'y_label': ['wall time [s]', r'real-time factor $T_{\mathrm{wall}}$'
                r'$T_{\mathrm{model}}$'],
    'fill_variables': [
        'frac_phase_communicate',
        'frac_phase_update',
        'frac_phase_deliver'],
    'time_scaling': 1e3
}


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
B.plot_main(axis=ax2)
B.plot_fractions(axis=ax3,
                 fill_variables=[
                     'frac_phase_communicate',
                     'frac_phase_update',
                     'frac_phase_deliver'])

ax1.set_xlabel('Number of Nodes')
ax3.set_xlabel('Number of Nodes')

ax1.legend()
ax2.legend()
ax3.legend()

plt.savefig('scaling.pdf')
