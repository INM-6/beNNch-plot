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
    'wall_time_create+wall_time_connect': light.light_cyan,
    'wall_time_phase_update': light.orange,
    'wall_time_phase_deliver': light.light_blue,
    'wall_time_phase_communicate': light.mint,
    'wall_time_phase_collocate': light.light_yellow,
    'frac_phase_update': light.orange,
    'frac_phase_deliver': light.light_blue,
    'frac_phase_communicate': light.mint,
    'frac_phase_collocate': light.light_yellow,
    'phase_update_factor': light.orange,
    'phase_deliver_factor': light.light_blue,
    'phase_communicate_factor': light.mint,
    'phase_collocate_factor': light.light_yellow,
    'total_memory': light.olive,
    'total_memory_per_node': light.pear,
}

label_params = {
    'threads_per_node': 'OMP threads',
    'tasks_per_node': 'MPI processes',
    'num_nodes': 'Nodes',
    'wall_time_total': 'Total',
    'wall_time_preparation': 'Preparation',
    'wall_time_presim': 'Presimulation',
    'wall_time_creation': 'Creation',
    'wall_time_connect': 'Connection',
    'wall_time_sim': 'State propagation',
    'wall_time_phase_total': 'All phases',
    'wall_time_phase_update': 'Update',
    'wall_time_phase_collocate': 'Collocation',
    'wall_time_phase_communicate': 'Communication',
    'wall_time_phase_deliver': 'Delivery',
    'wall_time_create+wall_time_connect': 'Network construction',
    'max_memory': 'Memory',
    'sim_factor': 'State propagation',
    'frac_phase_update': 'Update',
    'frac_phase_communicate': 'Communication',
    'frac_phase_deliver': 'Delivery',
    'frac_phase_collocate': 'Collocation',
    'phase_update_factor': 'Update',
    'phase_communicate_factor': 'Communication',
    'phase_deliver_factor': 'Delivery',
    'phase_collocate_factor': 'Collocation',
    'phase_total_factor': 'All phases',
    'total_memory': 'Memory',
    'total_memory_per_node': 'Memory per node',

}
