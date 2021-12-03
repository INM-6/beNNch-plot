"""
Class for benchmarking plots
"""

import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import gridspec
import numpy as np
import yaml
import os
try:
    from . import plot_params as pp
except ImportError:
    import plot_params as pp


class BenchPlot():
    """
    Class organizing benchmarking plots.

    Attributes
    ----------
    x_axis : str or list
        variable to be plotted on x-axis
    x_ticks : str, optional

    data_file : str, optional
        path to data
    matplotlib_params : dict, optional
        parameters passed to matplotlib
    color_params : dict, optional
        unique colors for variables
    additional_params : dict, optional
        additional parameters used for plotting
    label_params : dict, optional
        labels used when plotting
    time_scaling : int, optional
        scaling parameter for simulation time
   """

    def __init__(self, x_axis,
                 x_ticks='data',
                 data_file='/path/to/data',
                 matplotlib_params=pp.matplotlib_params,
                 color_params=pp.color_params,
                 additional_params=pp.additional_params,
                 label_params=pp.label_params,
                 time_scaling=1):

        self.x_axis = x_axis
        self.x_ticks = x_ticks
        self.matplotlib_params = matplotlib_params
        self.additional_params = additional_params
        self.color_params = color_params
        self.label_params = label_params
        self.time_scaling = time_scaling

        self.load_data(data_file)
        self.compute_derived_quantities()

    def load_data(self, data_file):
        """
        Load data to dataframe, to be used later when plotting.

        Group the data by specified operations.

        Attributes
        ----------
        data_file : str
            data file to be loaded and later plotted

        Raises
        ------
        ValueError
        """
        try:
            self.df = pd.read_csv(data_file, delimiter=',')
        except FileNotFoundError:
            print('File could not be found')
            quit()

        for py_timer in ['py_time_create', 'py_time_connect']:
            if py_timer not in self.df:
                self.df[py_timer] = np.nan
                raise ValueError('Warning! Python timers are not found. ' +
                                 'Construction time measurements will not ' +
                                 'be accurate.')

        dict_ = {'num_nodes': 'first',
                 'threads_per_task': 'first',
                 'tasks_per_node': 'first',
                 'model_time_sim': 'first',
                 'wall_time_create': ['mean', 'std'],
                 'wall_time_connect': ['mean', 'std'],
                 'wall_time_sim': ['mean', 'std'],
                 'wall_time_phase_collocate': ['mean', 'std'],
                 'wall_time_phase_communicate': ['mean', 'std'],
                 'wall_time_phase_deliver': ['mean', 'std'],
                 'wall_time_phase_update': ['mean', 'std'],
                 'wall_time_communicate_target_data': ['mean', 'std'],
                 'wall_time_gather_spike_data': ['mean', 'std'],
                 'wall_time_gather_target_data': ['mean', 'std'],
                 'wall_time_communicate_prepare': ['mean', 'std'],
                 'py_time_create': ['mean', 'std'],
                 'py_time_connect': ['mean', 'std'],
                 'base_memory': ['mean', 'std'],
                 'network_memory': ['mean', 'std'],
                 'init_memory': ['mean', 'std'],
                 'total_memory': ['mean', 'std'],
                 'num_connections': ['mean', 'std'],
                 'local_spike_counter': ['mean', 'std'],

                 }

        col = ['num_nodes', 'threads_per_task', 'tasks_per_node',
               'model_time_sim', 'wall_time_create',
               'wall_time_create_std', 'wall_time_connect',
               'wall_time_connect_std', 'wall_time_sim',
               'wall_time_sim_std', 'wall_time_phase_collocate',
               'wall_time_phase_collocate_std', 'wall_time_phase_communicate',
               'wall_time_phase_communicate_std', 'wall_time_phase_deliver',
               'wall_time_phase_deliver_std', 'wall_time_phase_update',
               'wall_time_phase_update_std',
               'wall_time_communicate_target_data',
               'wall_time_communicate_target_data_std',
               'wall_time_gather_spike_data',
               'wall_time_gather_spike_data_std',
               'wall_time_gather_target_data',
               'wall_time_gather_target_data_std',
               'wall_time_communicate_prepare',
               'wall_time_communicate_prepare_std',
               'py_time_create', 'py_time_create_std',
               'py_time_connect', 'py_time_connect_std',
               'base_memory', 'base_memory_std',
               'network_memory', 'network_memory_std',
               'init_memory', 'init_memory_std',
               'total_memory', 'total_memory_std',
               'num_connections', 'num_connections_std',
               'local_spike_counter', 'local_spike_counter_std']

        self.df = self.df.drop('rng_seed', axis=1).groupby(
            ['num_nodes',
             'threads_per_task',
             'tasks_per_node',
             'model_time_sim'], as_index=False).agg(dict_)
        self.df.columns = col

    def compute_derived_quantities(self):
        """
        Do computations to get parameters needed for plotting.
        """

        self.df['num_nvp'] = (
            self.df['threads_per_task'] * self.df['tasks_per_node']
        )
        self.df['model_time_sim'] /= self.time_scaling
        self.df['wall_time_create+wall_time_connect'] = (
            self.df['py_time_create'] + self.df['py_time_connect'])
        self.df['wall_time_create+wall_time_connect_std'] = (
            np.sqrt((self.df['wall_time_create_std']**2 +
                     self.df['wall_time_connect_std']**2)))
        self.df['sim_factor'] = (self.df['wall_time_sim'] /
                                 self.df['model_time_sim'])
        self.df['sim_factor_std'] = (self.df['wall_time_sim_std'] /
                                     self.df['model_time_sim'])
        self.df['wall_time_phase_total'] = (
            self.df['wall_time_phase_update'] +
            self.df['wall_time_phase_communicate'] +
            self.df['wall_time_phase_deliver'] +
            self.df['wall_time_phase_collocate'])
        self.df['wall_time_phase_total_std'] = \
            np.sqrt(
            self.df['wall_time_phase_update_std']**2 +
            self.df['wall_time_phase_communicate_std']**2 +
            self.df['wall_time_phase_deliver_std']**2 +
            self.df['wall_time_phase_collocate_std']**2
        )
        self.df['phase_total_factor'] = (
            self.df['wall_time_phase_total'] /
            self.df['model_time_sim'])
        self.df['phase_total_factor_std'] = (
            self.df['wall_time_phase_total_std'] /
            self.df['model_time_sim'])

        for phase in ['update', 'communicate', 'deliver', 'collocate']:
            self.df['phase_' + phase + '_factor'] = (
                self.df['wall_time_phase_' + phase] /
                self.df['model_time_sim'])

            self.df['phase_' + phase + '_factor' + '_std'] = (
                self.df['wall_time_phase_' + phase + '_std'] /
                self.df['model_time_sim'])

            self.df['frac_phase_' + phase] = (
                100 * self.df['wall_time_phase_' + phase] /
                self.df['wall_time_phase_total'])

            self.df['frac_phase_' + phase + '_std'] = (
                100 * self.df['wall_time_phase_' + phase + '_std'] /
                self.df['wall_time_phase_total'])
        self.df['total_memory_per_node'] = (self.df['total_memory'] /
                                            self.df['num_nodes'])
        self.df['total_memory_per_node_std'] = (self.df['total_memory_std'] /
                                                self.df['num_nodes'])

    def plot_fractions(self, axis, fill_variables,
                       interpolate=False, step=None, log=False, alpha=1.,
                       error=False):
        """
        Fill area between curves.

        axis : Matplotlib axes object
        fill_variables : list
            variables (e.g. timers) to be plotted as fill  between graph and
            x axis
        interpolate : bool, default
            whether to interpolate between the curves
        step : {'pre', 'post', 'mid'}, optional
            should the filling be a step function
        log : bool, default
            whether the x-axes should have logarithmic scale
        alpha, int, default
            alpha value of fill_between plot
        error : bool
            whether plot should have error bars
        """

        fill_height = 0
        for fill in fill_variables:
            axis.fill_between(np.squeeze(self.df[self.x_axis]),
                              fill_height,
                              np.squeeze(self.df[fill]) + fill_height,
                              label=self.label_params[fill],
                              facecolor=self.color_params[fill],
                              interpolate=interpolate,
                              step=step,
                              alpha=alpha,
                              linewidth=0.5,
                              edgecolor='#444444')
            if error:
                axis.errorbar(np.squeeze(self.df[self.x_axis]),
                              np.squeeze(self.df[fill]) + fill_height,
                              yerr=np.squeeze(self.df[fill + '_std']),
                              capsize=3,
                              capthick=1,
                              color='k',
                              fmt='none'
                              )
            fill_height += self.df[fill].to_numpy()

        if self.x_ticks == 'data':
            axis.set_xticks(np.squeeze(self.df[self.x_axis]))
        else:
            axis.set_xticks(self.x_ticks)

        if log:
            axis.set_xscale('log')
            axis.tick_params(bottom=False, which='minor')
            axis.get_xaxis().set_major_formatter(
                matplotlib.ticker.ScalarFormatter())

    def plot_main(self, quantities, axis, log=(False, False),
                  error=False, fmt='none'):
        """
        Main plotting function.

        Attributes
        ----------
        quantities : list
            list with plotting quantities
        axis : axis object
            axis object used when plotting
        log : tuple of bools, default
            whether x and y axis should have logarithmic scale
        error : bool, default
            whether or not to plot error bars
        fmt : string
            matplotlib format string (fmt) for defining line style
        """

        for y in quantities:
            if not error:
                axis.plot(self.df[self.x_axis],
                          self.df[y],
                          marker=None,
                          label=self.label_params[y],
                          color=self.color_params[y],
                          linewidth=2)
            else:
                axis.errorbar(
                    self.df[self.x_axis].values,
                    self.df[y].values,
                    yerr=self.df[y + '_std'].values,
                    marker=None,
                    capsize=3,
                    capthick=1,
                    label=self.label_params[y],
                    color=self.color_params[y],
                    fmt=fmt)

        if self.x_ticks == 'data':
            axis.set_xticks(self.df[self.x_axis].values)
        else:
            axis.set_xticks(self.x_ticks)

        if log[0]:
            axis.set_xscale('log')
        if log[1]:
            axis.tick_params(bottom=False, which='minor')
            axis.set_yscale('log')

    def merge_legends(self, ax1, ax2):
        """
        Merge legends from two axes, display them in the first

        Attributes
        ----------
        ax1 : axes object
            first axis
        ax2 : axes object
            second axis
        """
        handles, labels = [(a + b) for a, b in zip(
            ax2.get_legend_handles_labels(),
            ax1.get_legend_handles_labels())]
        ax1.legend(handles, labels, loc='upper right')

    def simple_axis(self, ax):
        """
        Remove top and right spines.

        Attributes
        ----------
        ax : axes object
            axes object for which to adjust spines
        """
        # Hide the right and top spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Only show ticks on the left and bottom spines
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
