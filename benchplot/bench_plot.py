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
    '''
    Class organizing benchmarking plots

    Attributes
    ----------
    data_hash : str or list
        unique identifier of experiment to be plotted
    x_axis : str or list
        variable to be plotted on x-axis
    log_axes : tuple of bools
        display x, y axis in log scale

    matplotlib_params : dict
        parameters passed to matplotlib
    color_params : dict
        unique colors for variables
    additional_params : dict
        additional parameters used for plotting
   '''

    def __init__(self, x_axis,
                 log_axes=(False, False),
                 hlines=None,
                 hline_colors=None,
                 vlines=None,
                 vline_colors=None,
                 x_ticks='data',
                 data_hash=None,
                 data_path='/path/to/data',
                 catalogue_path='/path/to/catalogue.yaml',
                 matplotlib_params=pp.matplotlib_params,
                 color_params=pp.color_params,
                 additional_params=pp.additional_params,
                 label_params=pp.label_params,
                 manually_set_plot_name=None,
                 time_scaling=1):
        '''
        Initialize attributes. Use attributes to set up figure.
        '''

        self.hlines = hlines
        self.hline_colors = hline_colors
        self.vlines = vlines
        self.vline_colors = vline_colors
        self.x_axis = x_axis
        self.x_ticks = x_ticks
        self.matplotlib_params = matplotlib_params
        self.additional_params = additional_params
        self.color_params = color_params
        self.label_params = label_params
        self.time_scaling = time_scaling

        self.load_data(data_hash, data_path, catalogue_path,
                       manually_set_plot_name)
        self.compute_derived_quantities()

    def load_data(self, data_hash, data_path, catalogue_path,
                  manually_set_plot_name):
        if data_hash is None:
            # data path points directly to file
            try:
                self.df = pd.read_csv(data_path, delimiter=',')
            except FileNotFoundError:
                print('File could not be found')
                quit()
        else:
            with open(catalogue_path, 'r') as c:
                catalogue = yaml.safe_load(c)
            self.plot_name = catalogue[data_hash]['plot_name']

            data_path = os.path.join(data_path, data_hash + '.csv')

            try:
                self.df = pd.read_csv(data_path, delimiter=';')
            except FileNotFoundError:
                print('File could not be found')
                quit()

        if manually_set_plot_name is not None:
            self.plot_name = manually_set_plot_name

    def compute_derived_quantities(self):
        self.df['num_nvp'] = (
            self.df['num_omp_threads'] * self.df['num_mpi_tasks']
        )
        self.df['model_time_sim'] /= self.time_scaling
        self.df['wall_time_creation+wall_time_connect'] = (
            self.df['wall_time_creation'] + self.df['wall_time_connect'])
        self.df['sim_factor'] = (self.df['wall_time_sim']
                                 / self.df['model_time_sim'])
        self.df['phase_total_factor'] = (self.df['wall_time_phase_total']
                                         / self.df['model_time_sim'])
        self.df['phase_update_factor'] = (self.df['wall_time_phase_update']
                                          / self.df['model_time_sim'])
        self.df['phase_communicate_factor'] = (self.df[
            'wall_time_phase_communicate']
            / self.df['model_time_sim'])
        self.df['phase_deliver_factor'] = (self.df['wall_time_phase_deliver']
                                           / self.df['model_time_sim'])

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

    def plot_fractions(self, axis, fill_variables,
                       interpolate=False, step='pre', log=False):
        '''
        fill_variables : list
            variables (e.g. timers) to be plotted as fill  between graph and
            x axis
        '''
        fill_height = 0
        for fill in fill_variables:
            axis.fill_between(np.squeeze(self.df[self.x_axis]),
                              fill_height,
                              np.squeeze(self.df[fill]) + fill_height,
                              label=self.label_params[fill],
                              color=self.color_params[fill],
                              interpolate=interpolate,
                              step=step)
            fill_height += self.df[fill].to_numpy()

        axis.set_ylabel(r'$T_{\mathrm{wall}} \: [\%]$')

        if self.x_ticks == 'data':
            axis.set_xticks(np.squeeze(self.df[self.x_axis]))
        else:
            axis.set_xticks(self.x_ticks)

        if log:
            axis.set_xscale('log')
            axis.tick_params(bottom=False, which='minor')
            axis.get_xaxis().set_major_formatter(
                matplotlib.ticker.ScalarFormatter())

    def plot_main(self, quantities, axis, log=(False, False)):
        for y in quantities:
            axis.plot(self.df[self.x_axis],
                      self.df[y],
                      marker='o',
                      label=self.label_params[y],
                      color=self.color_params[y])

        if self.x_ticks == 'data':
            axis.set_xticks(self.df[self.x_axis].values)
        else:
            axis.set_xticks(self.x_ticks)

        if log[0]:
            axis.set_xscale('log')
        if log[1]:
            axis.tick_params(bottom=False, which='minor')
            axis.set_yscale('log')

        # plot horizontal line(s)
        if self.hlines is not None:
            for i, hline in enumerate(self.hlines[plot_column]):
                axis.axhline(hline, color=self.hline_colors[i])

        # plot vertical line(s)
        if self.vlines is not None:
            for i, vline in enumerate(self.vlines):
                axis.axvline(vline, color=self.vline_colors[i])

    def merge_legends(self, ax1, ax2):
        handles, labels = [(a + b) for a, b in zip(
            ax2.get_legend_handles_labels(),
            ax1.get_legend_handles_labels())]
        ax1.legend(handles, labels, loc='upper right')
        ax1.set_xticklabels('')



