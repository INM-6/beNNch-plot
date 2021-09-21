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
    'wall_time_total': 'total',
    'wall_time_preparation': 'preparation',
    'wall_time_presim': 'presimulation',
    'wall_time_creation': 'creation',
    'wall_time_connect': 'connection',
    'wall_time_sim': 'state propagation',
    'wall_time_phase_total': 'all phases',
    'wall_time_phase_update': 'update',
    'wall_time_phase_collocate': 'collocation',
    'wall_time_phase_communicate': 'communication',
    'wall_time_phase_deliver': 'delivery',
    'wall_time_create+wall_time_connect': 'network construction',
    'max_memory': 'memory',
    'sim_factor': 'state propagation',
    'frac_phase_update': 'update',
    'frac_phase_communicate': 'communication',
    'frac_phase_deliver': 'delivery',
    'frac_phase_collocate': 'collocation',
    'phase_update_factor': 'update',
    'phase_communicate_factor': 'communication',
    'phase_deliver_factor': 'delivery',
    'phase_collocate_factor': 'collocation',
    'phase_total_factor': 'all phases',
    'total_memory': 'memory',
    'total_memory_per_node': 'memory per node',

}
