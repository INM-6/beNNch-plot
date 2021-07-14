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
}

bright = tol_colors.tol_cset('bright')
vibrant = tol_colors.tol_cset('vibrant')
light = tol_colors.tol_cset('light')

color_params = {
    'wall_time_total': light.pale_grey,
    'sim_factor': light.pink,
    'phase_total_factor': light.orange,
    'wall_time_sim': light.pink,
    'wall_time_creation+wall_time_connect': light.light_cyan,
    'frac_phase_communicate': light.mint,
    'wall_time_phase_communicate': light.mint,
    'phase_communicate_factor': light.mint,
    'wall_time_phase_update': light.orange,
    'frac_phase_update': light.orange,
    'phase_update_factor': light.orange,
    'wall_time_phase_deliver': light.light_blue,
    'frac_phase_deliver': light.light_blue,
    'phase_deliver_factor': light.light_blue,
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
    'wall_time_sim': 'state propagation',
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
    'phase_update_factor': 'update',
    'phase_communicate_factor': 'communicate',
    'phase_deliver_factor': 'deliver',
    'phase_total_factor': 'all phases'
}
