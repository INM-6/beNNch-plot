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
        variables (e.g. timers) to be plotted as fill  between graph and
        x axis
    matplotlib_params : dict
        parameters passed to matplotlib
    color_params : dict
        unique colors for variables
    additional_params : dict
        additional parameters used for plotting
   '''

    def __init__(self, x_axis, y_axis, x_label, y_label, fill_variables,
                 log_axes=(False, False),
                 hlines=None,
                 hline_colors=None,
                 vlines=None,
                 vline_colors=None,
                 x_ticks='data',
                 ylims=None,
                 data_hash=None,
                 data_path='/path/to/data',
                 catalogue_path='/path/to/catalogue.yaml',
                 save_path='/path/to/save/plots',
                 file_ending='pdf',
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
        self.y_axis = y_axis
        self.x_label = x_label
        self.y_label = y_label
        self.log_axes = log_axes
        self.fill_variables = fill_variables
        self.x_ticks = x_ticks
        self.ylims = ylims
        self.save_path = save_path
        self.file_ending = file_ending
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

    def setup_figure(self, num_subplots):
        # Change matplotlib defaults
        matplotlib.rcParams.update(self.matplotlib_params)

        if num_subplots == 1:
            figsize = self.additional_params['figsize_single']
        elif num_subplots == 2:
            figsize = self.additional_params['figsize_double']

        # Set up figure
        self.fig = plt.figure(figsize=figsize)
        self.st = self.fig.suptitle(self.plot_name)
        self.spec = gridspec.GridSpec(ncols=num_subplots, nrows=4,
                                      figure=self.fig)

    def plot_fractions(self, axis, fill_variables=None,
                       interpolate=False, step='pre'):
        fill_height = 0
        if fill_variables is None:
            fill_variables = self.fill_variables
        for fill in fill_variables:
            axis.fill_between(np.squeeze(self.df[self.x_axis]),
                              fill_height,
                              np.squeeze(self.df[fill]) + fill_height,
                              label=self.label_params[fill],
                              color=self.color_params[fill],
                              interpolate=interpolate,
                              step=step)
            fill_height += self.df[fill].to_numpy()

        if self.x_ticks == 'data':
            axis.set_xticks(np.squeeze(self.df[self.x_axis]))
        else:
            axis.set_xticks(self.x_ticks)

        if self.log_axes[0]:
            axis.set_xscale('log')
            axis.tick_params(bottom=False, which='minor')
            axis.get_xaxis().set_major_formatter(
                matplotlib.ticker.ScalarFormatter())

        axis.set_xlabel(self.x_label)
        axis.set_ylabel(r'$T_{\mathrm{wall}}\%$')

        return axis

    def plot_main(self, axis, plot_column=0):
        for y in self.y_axis[plot_column]:
            axis.plot(self.df[self.x_axis],
                      self.df[y],
                      marker='o',
                      label=self.label_params[y],
                      color=self.color_params[y])
            axis.set_ylabel(self.y_label[plot_column])

        if self.x_ticks == 'data':
            axis.set_xticks(self.df[self.x_axis].values)
        else:
            axis.set_xticks(self.x_ticks)

        if self.log_axes[0]:
            axis.tick_params(bottom=False, which='minor')
        if self.log_axes[1]:
            axis.set_yscale('log')

        if self.ylims is not None:
            axis.set_ylim(self.ylims[plot_column])

        # plot horizontal line(s)
        if self.hlines is not None:
            for i, hline in enumerate(self.hlines[plot_column]):
                axis.axhline(hline, color=self.hline_colors[i])

        # plot vertical line(s)
        if self.vlines is not None:
            for i, vline in enumerate(self.vlines):
                axis.axvline(vline, color=self.vline_colors[i])

        return axis

    def plot_single(self):
        self.setup_figure(1)
        # Plot fraction of times spent in phases
        self.plot_fractions(self.fig.add_subplot(self.spec[-1, 0]),
                            self.fill_variables)

        # Plot values specified in y_axis
        main_plot = self.plot_main(self.fig.add_subplot(self.spec[:-1, 0]), 0)
        main_plot.set_xticklabels('')

        self.finish_plot()

    def plot_double(self):
        self.setup_figure(2)
        # Plot fraction of times spent in phases
        frac_plot = self.plot_fractions(
            self.fig.add_subplot(self.spec[-1, 1]),
            self.fill_variables)

        # Plot values specified in y_axis
        main_plot = []
        if ('wall_time_sim' in self.y_axis[0] and
                'wall_time_creation+wall_time_connect' in self.y_axis[0]):
            main_plot.append(self.plot_fractions(
                self.fig.add_subplot(self.spec[:, 0]),
                fill_variables=['wall_time_sim',
                                'wall_time_creation+wall_time_connect'],
                interpolate=True, step=None))
            self.y_axis[0].remove('wall_time_sim')
            self.y_axis[0].remove('wall_time_creation+wall_time_connect')
            if self.y_axis[0]:
                main_plot[0] = self.plot_main(main_plot[0])
        else:
            main_plot.append(self.plot_main(self.fig.add_subplot(
                self.spec[:, 0], sharex=frac_plot), plot_column=0))
        main_plot[0].set_xlabel(self.x_label)
        main_plot[0].legend(loc='upper right')

        main_plot.append(self.plot_main(self.fig.add_subplot(
            self.spec[:-1, 1]), plot_column=1))

        handles, labels = [(a + b) for a, b in zip(
            frac_plot.get_legend_handles_labels(),
            main_plot[1].get_legend_handles_labels())]
        main_plot[1].legend(handles, labels, loc='upper right')
        main_plot[1].set_xticklabels('')

        self.finish_plot()

    def finish_plot(self):
        plt.tight_layout()
        self.st.set_y(0.95)
        self.fig.subplots_adjust(top=0.87)

    def save_fig(self):
        plt.savefig(os.path.join(self.save_path,
                                 self.plot_name + '.' + self.file_ending))
