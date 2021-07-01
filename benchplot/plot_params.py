import tol_colors

size_factor = 1.3
matplotlib_params = {
    'text.latex.preamble': ['\\usepackage{gensymb}'],
    'image.origin': 'lower',
    'image.interpolation': 'nearest',
    'axes.grid': False,
    'axes.labelsize': 15*size_factor,
    'axes.titlesize': 19*size_factor,
    'font.size': 16*size_factor,
    'legend.fontsize': 11*size_factor,
    'xtick.labelsize': 11*size_factor,
    'ytick.labelsize': 11*size_factor,
    # 'font.family': 'sans-serif',
    # 'font.sans-serif': 'Avenir',
    'text.usetex': False,
}

additional_params = {
    'figsize_single': [6.1 * 1.5, 6.1],
    'figsize_double': [12.2, 6.1*1.1]
    # 'figsize_double': [12.2*1.5, 6.1]
}

bright = tol_colors.tol_cset('bright')
vibrant = tol_colors.tol_cset('vibrant')

color_params = {
    'wall_time_total': bright.grey,
    'sim_factor': bright.purple,
    'phase_total_factor': vibrant.orange,
    'wall_time_sim': bright.purple,
    'wall_time_create+wall_time_connect': bright.cyan,
    'py_time_create+py_time_connect': bright.cyan,
    'wall_time_phase_update': bright.red,
    'wall_time_phase_deliver': vibrant.blue,
    'wall_time_phase_communicate': bright.green,
    'wall_time_phase_collocate': bright.yellow,
    'frac_phase_update': bright.red,
    'frac_phase_deliver': vibrant.blue,
    'frac_phase_communicate': bright.green,
    'frac_phase_collocate': bright.yellow,
}

label_params = {
    'threads_per_node': 'OMP threads',
    'tasks_per_node': 'MPI processes',
    'num_nodes': 'Nodes',
    'wall_time_total': 'total',
    'wall_time_preparation': 'preparation',
    'wall_time_presim': 'presimulation',
    'wall_time_creation': 'creation',
    'wall_time_connect': 'connection',
    'wall_time_sim': 'state propagation',
    'wall_time_phase_total': 'all phases',
    'wall_time_phase_update': 'update',
    'wall_time_phase_collocate': 'collocate',
    'wall_time_phase_communicate': 'communicate',
    'wall_time_phase_deliver': 'deliver',
    'wall_time_create+wall_time_connect': 'network construction',
    'py_time_create+py_time_connect': 'network construction',
    'max_memory': 'memory',
    'sim_factor': 'state propagation',
    'frac_phase_update': 'update',
    'frac_phase_communicate': 'communicate',
    'frac_phase_deliver': 'deliver',
    'frac_phase_collocate': 'collocate',
    'phase_update_factor': 'update factor',
    'phase_communicate_factor': 'communicate factor',
    'phase_deliver_factor': 'deliver factor',
    'phase_collocate_factor': 'collocate factor',
    'phase_total_factor': 'all phases'
}
