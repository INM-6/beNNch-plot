import benchplot as bp
import tol_colors
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


vibrant = tol_colors.tol_cset('vibrant')

hashes = ['0a6f610e-824d-11eb-8289-57dd6a14c4b8',
          '700c9db6-824c-11eb-adb7-67ae217a4502',
          'ef8839ce-824c-11eb-aa99-4bdf3bfd375d',
          '01e23ea8-824d-11eb-83c5-8f9f7c8aec93']

label_params_y = [{'sim_factor' : '1 MPI Process, 128 Threads p. Process',
                   'max_memory' : '1 MPI Process, 128 Threads p. Process'},
                  {'sim_factor' : '2 MPI Processes, 64 Threads p. Process',
                   'max_memory' : '2 MPI Processes, 64 Threads p. Process'},
                  {'sim_factor' : '4 MPI Processes, 32 Threads p. Process',
                   'max_memory' : '4 MPI Processes, 32 Threads p. Process'},
                  {'sim_factor' : '8 MPI Processes, 16 Threads p. Process',
                   'max_memory' : '8 MPI Processes, 16 Threads p. Process'}]

color_params = [{'sim_factor' : vibrant.orange,
                 'max_memory' : vibrant.orange},
                {'sim_factor' : vibrant.blue,
                 'max_memory' : vibrant.blue},
                {'sim_factor' : vibrant.cyan,
                 'max_memory' : vibrant.cyan},
                {'sim_factor' : vibrant.magenta,
                 'max_memory' : vibrant.magenta}]

arg_template = {'data_path' : './results_microcircuit_jusuf',
                'catalogue_path' : 'catalogue_microcircuit_jusuf.yaml',
                'save_path' : './',
                'manually_set_plot_name' : 'Microcircuit Comparison',
                'hlines' : [[1],[]],
                'hline_colors' : ['red'],
                'x_axis' : ['num_nodes'],
                'y_axis' : [['sim_factor'], ['max_memory']],
                'x_label' : ['Nodes'],
                'y_label' : [r'real-time factor $T_{\mathrm{wall}}/$'
                             '$T_{\mathrm{model}}$', 'Memory'],
                'fill_variables' : [],
                'time_scaling' : 1e3
               }

# Generate argument dicts
args = []
for i, data_hash in enumerate(hashes):
    arg = arg_template.copy()
    arg['data_hash'] = data_hash
    arg['label_params'] = label_params_y[i]
    arg['color_params'] = color_params[i]

    args.append(arg)


# Instantiate objectes
benchplots = []
for arg in args:
    B = bp.BenchPlot(**arg)
    benchplots.append(B)

# Plotting
fig = plt.figure(figsize= (12, 6), constrained_layout=True)
spec = gridspec.GridSpec(ncols=2, nrows=1, figure=fig)

ax1 = fig.add_subplot(spec[0, 0])
ax2 = fig.add_subplot(spec[0, 1])


for B in benchplots:
    B.plot_main(axis=ax1, plot_column=0)
    B.plot_main(axis=ax2, plot_column=1)

ax1.set_xlabel('Number of Nodes')
ax2.set_xlabel('Number of Nodes')

ax1.legend()
ax2.legend()

plt.savefig('microcircuit_jusuf_scaling.pdf')

