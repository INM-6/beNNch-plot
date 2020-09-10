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
    'text.usetex': True,
    'font.family': 'serif',
}

additional_params = {
    'figsize_single': [6.1, 6.1/3],
    'figsize_double': [12.2, 12.2/3]
}

color_params = {
    'wall_time_total': '#bebebe', # Black
    'wall_time_sim': '#ff9f9a', # Peach
    'wall_time_creation+wall_time_connect': '#64b5cd', # Light Blue
    'wall_time_phase_update': '#c44e52', # Brownish red
    'wall_time_phase_deliver': '#4c72b0', # Dark Blue
    'wall_time_phase_communicate': '#55a868', # Light green
    }

label_params = {
    'num_omp_threads': 'OMP threads',
    'num_mpi_tasks': 'MPI processes',
    'num_nodes': 'Nodes',
    'wall_time_total': 'wall time [s]',
    'wall_time_preparation': 'wall time preparation [s]',
    'wall_time_presim': 'presimulation time',
    'wall_time_creation': 'creation time',
    'wall_time_connect': 'connection time',
    'wall_time_sim': 'simulation time',
    'wall_time_phase_total': 'total phase time',
    'wall_time_phase_update': 'update',
    'wall_time_phase_collocate': 'collocate',
    'wall_time_phase_communicate': 'communicate',
    'wall_time_phase_deliver': 'deliver',
    'max_memory': 'memory',
    'real_time_factor': 'real time factor',
    'phase_update_factor': 'update factor',
    'phase_communicate_factor': 'communicate factor',
    'phase_deliver_factor': 'deliver factor',
}