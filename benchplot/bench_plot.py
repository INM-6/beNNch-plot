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
                self.df = pd.read_csv(data_path, delimiter=',')
            except FileNotFoundError:
                print('File could not be found')
                quit()

        if manually_set_plot_name is not None:
            self.plot_name = manually_set_plot_name

        for py_timer in ['py_time_prepare', 'py_time_network_local',
                         'py_time_network_global', 'py_time_init',
                         'py_time_simulate', 'py_time_create',
                         'py_time_connect']:
            if py_timer not in self.df:
                self.df[py_timer] = np.nan

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
                 'py_time_prepare': ['mean', 'std'],
                 'py_time_network_local': ['mean', 'std'],
                 'py_time_network_global': ['mean', 'std'],
                 'py_time_init': ['mean', 'std'],
                 'py_time_simulate': ['mean', 'std'],
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
               'py_time_prepare', 'py_time_prepare_std',
               'py_time_network_local', 'py_time_network_local_std',
               'py_time_network_global', 'py_time_network_global_std',
               'py_time_init', 'py_time_init_std',
               'py_time_simulate', 'py_time_simulate_std',
               'py_time_create', 'py_time_create_std',
               'py_time_connect', 'py_time_connect_std',
               'base_memory', 'base_memory_std',
               'network_memory', 'network_memory_std',
               'init_memory', 'init_memory_std',
               'total_memory', 'total_memory_std',
               'num_connections', 'num_connections_std',
               'local_spike_counter', 'local_spike_counter_std']

        self.df = self.df[~self.df['wall_time_communicate_target_data'].isna(
        )].reset_index().drop('index', axis=1)
        self.df = self.df.drop('MASTER_SEED', axis=1).groupby(
            ['num_nodes',
             'threads_per_task',
             'tasks_per_node',
             'model_time_sim'], as_index=False).agg(dict_)
        self.df.columns = col

    def compute_derived_quantities(self):
        self.df['num_nvp'] = (
            self.df['threads_per_task'] * self.df['tasks_per_node']
        )
        self.df['model_time_sim'] /= self.time_scaling
        self.df['wall_time_create+wall_time_connect'] = (
            self.df['py_time_create'] + self.df['py_time_connect'])
        self.df['wall_time_create+wall_time_connect_std'] = (
            np.sqrt((self.df['wall_time_create_std']**2
                     + self.df['wall_time_connect_std']**2)))
        self.df['sim_factor'] = (self.df['wall_time_sim']
                                 / self.df['model_time_sim'])
        self.df['sim_factor_std'] = (self.df['wall_time_sim_std']
                                     / self.df['model_time_sim'])
        self.df['wall_time_phase_total'] = (
            self.df['wall_time_phase_update']
            + self.df['wall_time_phase_communicate']
            + self.df['wall_time_phase_deliver']
            + self.df['wall_time_phase_collocate'])
        self.df['wall_time_phase_total_std'] = \
            np.sqrt(
            self.df['wall_time_phase_update_std']**2
            + self.df['wall_time_phase_communicate_std']**2
            + self.df['wall_time_phase_deliver_std']**2
            + self.df['wall_time_phase_collocate_std']**2
        )
        self.df['phase_total_factor'] = (
            self.df['wall_time_phase_total']
            / self.df['model_time_sim'])
        self.df['phase_total_factor_std'] = (
            self.df['wall_time_phase_total_std']
            / self.df['model_time_sim'])

        for phase in ['update', 'communicate', 'deliver', 'collocate']:
            self.df['phase_' + phase + '_factor'] = (
                self.df['wall_time_phase_' + phase]
                / self.df['model_time_sim'])

            self.df['phase_' + phase + '_factor' + '_std'] = (
                self.df['wall_time_phase_' + phase + '_std']
                / self.df['model_time_sim'])

            self.df['frac_phase_' + phase] = (
                100 * self.df['wall_time_phase_' + phase]
                / self.df['wall_time_phase_total'])

            self.df['frac_phase_' + phase + '_std'] = (
                100 * self.df['wall_time_phase_' + phase + '_std']
                / self.df['wall_time_phase_total'])

    def plot_fractions(self, axis, fill_variables,
                       interpolate=False, step='pre', log=False,
                       error=False):
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
            if error:
                axis.errorbar(np.squeeze(self.df[self.x_axis]),
                              np.squeeze(self.df[fill]) + fill_height,
                              yerr=np.squeeze(self.df[fill + '_std']),
                              capsize=3,
                              capthick=1,
                              color='k'
                              )
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
            axis.errorbar(
                self.df[self.x_axis].values,
                self.df[y].values,
                yerr=self.df[y + '_std'].values,
                marker='o',
                capsize=3,
                capthick=1,
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

    def merge_legends(self, ax1, ax2):
        handles, labels = [(a + b) for a, b in zip(
            ax2.get_legend_handles_labels(),
            ax1.get_legend_handles_labels())]
        ax1.legend(handles, labels, loc='upper right')
        # ax1.set_xticklabels('')
