import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import gridspec
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
    x_label : str or list
        label of x axis/axes
    y_label : str or list
        label of y axis/axes
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

    def __init__(self, data_hash, x_axis, y_axis, x_label, y_label, log_x_axis,
                 log_y_axis, fill_variables, x_ticks='data',
                 matplotlib_params=pp.matplotlib_params,
                 color_params=pp.color_params,
                 additional_params=pp.additional_params,
                 label_params=pp.label_params):
        '''
        Initialize attributes. Use attributes to set up figure.
        '''

        self.data_hash = data_hash
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.x_label = x_label
        self.y_label = y_label
        self.log_x_axis = log_x_axis
        self.log_y_axis = log_y_axis
        self.fill_variables = fill_variables
        self.x_ticks = x_ticks
        self.matplotlib_params = matplotlib_params
        self.color_params = color_params
        self.additional_params = additional_params
        self.label_params = label_params

        # Load data
        if type(data_hash) is str:
            data_hash = [data_hash]

        data_frames = []

        for dhash in data_hash:
            suffix = '/path/to/data.csv'
            data_path = os.path.join(dhash, suffix)
            data_path = 'multiareamodel_data.csv'
            # data_path = 'microcircuit_data.csv'

            try:
                data = pd.read_csv(data_path, delimiter=',')
            except FileNotFoundError:
                print('File could not be found')
                quit()

            data_frames.append(data)

        self.df = pd.concat(data_frames)

        # Compute derived quantities
        self.df['num_nvp'] = (
                self.df['num_omp_threads'] * self.df['num_mpi_tasks']
                )
        self.df['wall_time_creation+wall_time_connect'] = (
            self.df['wall_time_creation'] + self.df['wall_time_connect'])
        self.df['sim_factor'] = (self.df['wall_time_sim']
                                       / (self.df['model_time_sim']
                                          / 1000))  # ms to s
        self.df['phase_total_factor'] = (self.df['wall_time_phase_total']
                                       / (self.df['model_time_sim']
                                          / 1000))  # ms to s
        self.df['phase_update_factor'] = (self.df['wall_time_phase_update']
                                          / (self.df['model_time_sim']
                                             / 1000))  # ms to s
        self.df['phase_communicate_factor'] = (self.df[
            'wall_time_phase_communicate']
            / self.df['model_time_sim']
            / 1000)  # ms to s
        self.df['phase_deliver_factor'] = (self.df['wall_time_phase_deliver']
                                           / (self.df['model_time_sim']
                                              / 1000))  # ms to s

        self.df['frac_phase_update'] = (100 * self.df['wall_time_phase_update']
                                        / self.df['wall_time_phase_total'])
        self.df['frac_phase_communicate'] = (100
                                             * self.df[
                                                 'wall_time_phase_communicate']
                                             / self.df['wall_time_phase_total']
                                             )
        self.df['frac_phase_deliver'] = (100
                                         * self.df['wall_time_phase_deliver']
                                         / self.df['wall_time_phase_total'])

        # Change matplotlib defaults
        matplotlib.rcParams.update(matplotlib_params)

        # Determine number of subplots
        num_subplots = len(self.y_axis)
        if num_subplots == 1:
            figsize = additional_params['figsize_single']
        else:
            figsize = additional_params['figsize_double']

        # Set up figure
        fig = plt.figure(figsize=figsize)
        self.spec = gridspec.GridSpec(ncols=num_subplots, nrows=4, figure=fig)

        if num_subplots == 1:
            # Plot fraction of times spent in phases
            frac_plot = self.plot_fractions(fig.add_subplot(self.spec[-1, 0]))
            frac_plot.set_xlabel(self.x_label)
            frac_plot.set_ylabel(r'$T_{\textnormal{wall}}\%$')
            # Plot values specified in y_axis
            main_plot = self.plot_main(fig.add_subplot(
                self.spec[:-1, 0], sharex=frac_plot), plot_column=0)

        if num_subplots == 2:
            # Plot fraction of times spent in phases
            frac_plot = self.plot_fractions(fig.add_subplot(self.spec[-1, 1]))
            frac_plot.set_xlabel(self.x_label)
            frac_plot.set_ylabel(r'$T_{\textnormal{wall}}\%$')

            # Plot values specified in y_axis
            main_plot = self.plot_main(fig.add_subplot(
                self.spec[:-1, 1], sharex=frac_plot), plot_column=1)

            if ('wall_time_sim' in self.y_axis[0] and
                    'wall_time_creation+wall_time_connect' in self.y_axis[0]):
                main_plot_left = self.plot_fractions(
                    fig.add_subplot(self.spec[:, 0], sharex=frac_plot),
                    fill_variables=['wall_time_sim',
                                    'wall_time_creation+wall_time_connect'],
                    interpolate=True, step=None)
                self.y_axis[0].remove('wall_time_sim')
                self.y_axis[0].remove('wall_time_creation+wall_time_connect')
                if self.y_axis[0]:
                    main_plot_left = self.plot_main(main_plot_left)
            else:
                main_plot_left = self.plot_main(fig.add_subplot(
                    self.spec[:, 0], sharex=frac_plot), plot_column=0)
            main_plot_left.legend(loc='upper right')

        handles, labels = [(a + b) for a, b in zip(
            frac_plot.get_legend_handles_labels(),
            main_plot.get_legend_handles_labels())]
        main_plot.legend(handles, labels, loc='upper right')
        plt.tight_layout()
        plt.show()

    def plot_fractions(self, frac_plot, fill_variables=None, interpolate=False,
                       step='pre'):
        if fill_variables is None:
            fill_variables = self.fill_variables

        fill_height = 0
        for fill in fill_variables:
            frac_plot.fill_between(self.df[self.x_axis],
                                   fill_height,
                                   self.df[fill] + fill_height,
                                   label=self.label_params[fill],
                                   color=self.color_params[fill],
                                   interpolate=interpolate,
                                   step=step
                                   )
            fill_height += self.df[fill].to_numpy()

        if self.log_x_axis:
            frac_plot.set_xscale('log')
            frac_plot.tick_params(bottom=False, which='minor')
        frac_plot.get_xaxis().set_major_formatter(
            matplotlib.ticker.ScalarFormatter())
        if self.x_ticks == 'data':
            frac_plot.set_xticks(self.df[self.x_axis])
        else:
            frac_plot.set_xticks(self.x_ticks)

        return frac_plot

    def plot_main(self, main_plot, plot_column=0):
        for y in self.y_axis[plot_column]:
            main_plot.plot(self.df[self.x_axis],
                           self.df[y],
                           marker='o',
                           label=self.label_params[y],
                           color=self.color_params[y])
            main_plot.set_ylabel(self.y_label[plot_column])

        if self.log_x_axis:
            main_plot.tick_params(bottom=False, which='minor')
        if self.log_y_axis:
            main_plot.set_yscale('log')

        return main_plot


if __name__ == '__main__':

    # Bench_Plot(
    #     data_hash='trash',
    #     x_axis='num_omp_threads',
    #     y_axis=[['sim_factor']],
    #     x_label='Threads',
    #     y_label=[r'real-time factor $T_{\textnormal{wall}}'
    #              r'/T_{\textnormal{model}}$'],
    #     log_x_axis=True,
    #     log_y_axis=True,
    #     fill_variables=['frac_phase_update',
    #                     'frac_phase_communicate',
    #                     'frac_phase_deliver'],
    #     x_ticks=[1,2,4,8,16,32,64])

    Bench_Plot(
        data_hash='trash',
        x_axis='num_nodes',
        y_axis=[['wall_time_total', 'wall_time_sim',
                 'wall_time_creation+wall_time_connect'],
                ['sim_factor', 'phase_total_factor']],
        x_label='Nodes',
        y_label=['wall time [s]', r'real-time factor $T_{\textnormal{wall}}'
                 r'/T_{\textnormal{model}}$'],
        log_x_axis=False,
        log_y_axis=False,
        fill_variables=[
            'frac_phase_communicate',
            'frac_phase_update',
            'frac_phase_deliver'
        ])
