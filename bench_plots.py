import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import re
import os
import plot_params as pp


class Bench_Plot():
    '''
    Class organizing benchmarking plots

    Attributes
    ----------
    data_hash : str or list
        unique identifier of experiment to be plotted
    x_axis : str or list
        variable to be plotted on x-axis
    y_axis : str or list
        variable to be plotted
    log_x_axis : bool
        display x axis in log scale
    log_y_axis : book
        display y axis in log scale
    fill_variables : list
        variables (e.g. timers) to be plotted as fill  between graph and x axis
    matplotlib_params : dict
        parameters passed to matplotlib
    color_params : dict
        unique colors for variables
    additional_params : dict
        additional parameters used for plotting
   '''

    def __init__(self, data_hash, x_axis, y_axis, log_x_axis, log_y_axis,
                 fill_variables, matplotlib_params=pp.matplotlib_params,
                 color_params=pp.color_params,
                 additional_params=pp.additional_params,
                 label_params=pp.label_params):
        '''
        Initialize attributes. Use attributes to set up figure.
        '''
        # computing_resources = ['num_omp_threads',
        #                        'num_mpi_tasks',
        #                        'num_nodes']
        # measurements_general = ['wall_time_total',
        #                         'wall_time_preparation',
        #                         'wall_time_presim',
        #                         'wall_time_creation',
        #                         'wall_time_connect',
        #                         'wall_time_sim',
        #                         'wall_time_phase_total',
        #                         'wall_time_phase_update',
        #                         'wall_time_phase_collocate',
        #                         'wall_time_phase_communicate',
        #                         'wall_time_phase_deliver',
        #                         'max_memory']

        if type(y_axis) is str:
            y_axis = [y_axis]

        self.data_hash = data_hash
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.log_x_axis = log_x_axis
        self.log_y_axis = log_y_axis
        self.fill_variables = fill_variables
        self.matplotlib_params = matplotlib_params
        self.color_params = color_params
        self.additional_params = additional_params
        self.label_params=label_params

        # Load data
        if type(data_hash) is str:
            data_hash = [data_hash]

        data_frames = []

        for dhash in data_hash:
            suffix = '/path/to/data.csv'
            data_path = os.path.join(dhash, suffix)
            data_path = '/Users/work/Projects/MAM_benchmarking/BenchPlot/test.csv'

            try:
                data = pd.read_csv(data_path)
            except FileNotFoundError:
                print('File could not be found')
                quit()

            data_frames.append(data)

        self.df = pd.concat(data_frames)
        # import IPython
        # IPython.embed()
        # Compute derived quantities
        self.df['real_time_factor'] = (self.df['wall_time_total']
                                       / self.df['model_time_sim']
                                       / 1000)  # ms to s
        self.df['phase_update_factor'] = (self.df['wall_time_phase_update']
                                          / self.df['model_time_sim']
                                          / 1000)  # ms to s
        self.df['phase_communicate_factor'] = (self.df[
            'wall_time_phase_communicate']
            / self.df['model_time_sim']
            / 1000)  # ms to s
        self.df['phase_deliver_factor'] = (self.df['wall_time_phase_deliver']
                                           / self.df['model_time_sim']
                                           / 1000)  # ms to s

        # Change matplotlib defaults
        # update_matplotlib(matplotlib_params)
        matplotlib.rcParams.update(matplotlib_params)

        # Determine number of subplots
        num_subplots = len(y_axis)
        if num_subplots == 1:
            figsize = additional_params['figsize_single']
        else:
            figsize = additional_params['figsize_double']

        # Set up figure
        fig, ax = plt.subplots(1, num_subplots, figsize=figsize)

        if num_subplots > 1:
            for index, y in enumerate(y_axis):
                ax[index].plot(self.df[x_axis],
                               self.df[y],
                               label=self.label_params[y],
                               color=self.color_params[y])
        else:
            ax.plot(self.df[x_axis],
               self.df[y_axis[0]],
               label=self.label_params[y_axis[0]],
               color=self.color_params[y_axis[0]])
        plt.show()

if __name__ == '__main__':

    Bench_Plot(
        'trash',
        x_axis='num_nodes',
        y_axis=['wall_time_sim'],
        log_x_axis=False,
        log_y_axis=False,
        fill_variables=['wall_time_phase_communicate',
                        'wall_time_phase_update', 'wall_time_phase_deliver']
    )
