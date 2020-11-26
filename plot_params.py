matplotlib_params = {
    'text.latex.preamble': ['\\usepackage{gensymb}'],
    'image.origin': 'lower',
    'image.interpolation': 'nearest',
    'axes.grid': False,
    'axes.labelsize': 15,
    'axes.titlesize': 19,
    'font.size': 16,
    'legend.fontsize': 11,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'text.usetex': False,
    'font.family': 'serif',
}

additional_params = {
    'figsize_single': [6.1 * 1.5, 6.1],
    'figsize_double': [12.2, 6.1]
    # 'figsize_double': [12.2*1.5, 6.1]
}

# color_params = {
#     'wall_time_total': '#bebebe', # Black
#     'real_time_factor': '#bebebe', # Black
#     'wall_time_sim': '#ff9f9a', # Peach
#     'wall_time_creation+wall_time_connect': '#64b5cd', # Light Blue
#     'wall_time_phase_update': '#c44e52', # Brownish red
#     'wall_time_phase_deliver': '#4c72b0', # Dark Blue
#     'wall_time_phase_communicate': '#55a868', # Light green
#     'frac_phase_update': '#c44e52', # Brownish red
#     'frac_phase_deliver': '#4c72b0', # Dark Blue
#     'frac_phase_communicate': '#55a868', # Light green
#     }

color_params = {
    'wall_time_total': '#BBBBBB',  # gray
    'sim_factor': '#EE7733',  # orange
    'phase_total_factor': '#CCBB44',  # yellow
    'wall_time_sim': '#AA3377',  # purple
    'wall_time_creation+wall_time_connect': '#66CCEE',  # cyan
    'wall_time_phase_update': '#EE6677',  # red
    'wall_time_phase_deliver': '#0077BB',  # blue
    'wall_time_phase_communicate': '#228833',  # green
    'frac_phase_update': '#EE6677',  # red
    'frac_phase_deliver': '#0077BB',  # blue
    'frac_phase_communicate': '#228833',  # green
}

label_params = {
    'num_omp_threads': 'OMP threads',
    'num_mpi_tasks': 'MPI processes',
    'num_nodes': 'Nodes',
    'wall_time_total': 'total',
    'wall_time_preparation': 'preparation',
    'wall_time_presim': 'presimulation',
    'wall_time_creation': 'creation',
    'wall_time_connect': 'connection',
    'wall_time_sim': 'simulation',
    'wall_time_phase_total': 'all phases',
    'wall_time_phase_update': 'update',
    'wall_time_phase_collocate': 'collocate',
    'wall_time_phase_communicate': 'communicate',
    'wall_time_phase_deliver': 'deliver',
    'wall_time_creation+wall_time_connect': 'network construction',
    'max_memory': 'memory',
    'sim_factor': 'state propagation',
    'frac_phase_update': 'update',
    'frac_phase_communicate': 'communicate',
    'frac_phase_deliver': 'deliver',
    'phase_update_factor': 'update factor',
    'phase_communicate_factor': 'communicate factor',
    'phase_deliver_factor': 'deliver factor',
    'phase_total_factor': 'all phases'
}
