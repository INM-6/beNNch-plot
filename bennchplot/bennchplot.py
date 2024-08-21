"""
beNNch-plot - standardized plotting routines for performance benchmarks.
Copyright (C) 2021 Forschungszentrum Juelich GmbH, INM-6

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.

SPDX-License-Identifier: GPL-3.0-or-later
"""

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


class Plot():
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
                 time_scaling=1,
                 df=None):

        self.x_axis = x_axis
        self.x_ticks = x_ticks
        self.matplotlib_params = matplotlib_params
        self.additional_params = additional_params
        self.color_params = color_params
        self.label_params = label_params
        self.time_scaling = time_scaling

        self.df = df
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
        if self.df is None:
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
                 'completion_time': 'first',
                 'simulator_version': 'first',
                 'time_construction_create': ['mean', 'std'],
                 'time_construction_connect': ['mean', 'std'],
                 'time_simulate': ['mean', 'std'],
                 'time_collocate_spike_data': ['mean', 'std'],
                 'time_communicate_spike_data': ['mean', 'std'],
                 'time_deliver_spike_data': ['mean', 'std'],
                 'time_update': ['mean', 'std'],
                 'time_communicate_target_data': ['mean', 'std'],
                 'time_gather_spike_data': ['mean', 'std'],
                 'time_gather_target_data': ['mean', 'std'],
                 'time_communicate_prepare': ['mean', 'std'],
                 'py_time_create': ['mean', 'std'],
                 'py_time_connect': ['mean', 'std'],
                 'base_memory': ['mean', 'std'],
                 'network_memory': ['mean', 'std'],
                 'init_memory': ['mean', 'std'],
                 'total_memory': ['mean', 'std'],
                 'num_connections': ['mean', 'std']}

        col = ['num_nodes', 'threads_per_task', 'tasks_per_node',
               'model_time_sim', 'completion_time', 'simulator_version'
               'wall_time_create', 'wall_time_create_std', 'wall_time_connect',
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
               'num_connections', 'num_connections_std']

        self.df = self.df.drop('rng_seed', axis=1).groupby(
            ['num_nodes',
             'threads_per_task',
             'tasks_per_node',
             'model_time_sim',
             'completion_time',
             'simulator_version'], as_index=False).agg(dict_)
        print(self.df)
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
            axis.fill_between(self.df[self.x_axis].to_numpy().squeeze(axis=1),
                              fill_height,
                              self.df[fill].to_numpy() + fill_height,
                              label=self.label_params[fill],
                              facecolor=self.color_params[fill],
                              interpolate=interpolate,
                              step=step,
                              alpha=alpha,
                              linewidth=0.5,
                              edgecolor='#444444')
            if error:
                axis.errorbar(self.df[self.x_axis].to_numpy().squeeze(axis=1),
                              self.df[fill].to_numpy() + fill_height,
                              yerr=self.df[fill + '_std'].to_numpy(),
                              capsize=3,
                              capthick=1,
                              color='k',
                              fmt='none')
            fill_height += self.df[fill].to_numpy()

        if self.x_ticks == 'data':
            axis.set_xticks(self.df[self.x_axis].to_numpy().squeeze(axis=1))
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
                axis.plot(self.df[self.x_axis].to_numpy().squeeze(axis=1),
                          self.df[y].to_numpy(),
                          marker=None,
                          label=self.label_params[y],
                          color=self.color_params[y],
                          linewidth=2)
            else:
                axis.errorbar(
                    self.df[self.x_axis].to_numpy().squeeze(axis=1),
                    self.df[y].to_numpy(),
                    yerr=self.df[y + '_std'].to_numpy(),
                    marker=None,
                    capsize=3,
                    capthick=1,
                    label=self.label_params[y],
                    color=self.color_params[y],
                    fmt=fmt)

        if self.x_ticks == 'data':
            axis.set_xticks(self.df[self.x_axis].to_numpy().squeeze(axis=1))
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
