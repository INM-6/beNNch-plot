import benchplot as bp


bench = bp.BenchPlot(
    data_path='multi-area-model.csv',
    save_path='./',
    manually_set_plot_name='MAM',
    hlines=[[150], [15]],
    hline_colors=['red'],
    vlines=[30, 50],
    vline_colors=['gray', 'yellow'],
    file_ending='png',
    x_axis='num_nodes',
    y_axis=[['wall_time_total', 'wall_time_sim',
             'wall_time_creation+wall_time_connect'],
            ['sim_factor', 'phase_total_factor']],
    x_label='Nodes',
    y_label=['wall time [s]', r'real-time factor $T_{\mathrm{wall}}$'
             r'$T_{\mathrm{model}}$'],
    fill_variables=[
        'frac_phase_communicate',
        'frac_phase_update',
        'frac_phase_deliver'],
    )
bench.plot_double()
bench.save_fig()
