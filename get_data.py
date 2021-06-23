import sys
import yaml
import shutil
import subprocess
import os

import benchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec




jube_bench_path = str(sys.argv[1])
jube_id = str(sys.argv[2])
overwrite = str(sys.argv[3])
subprocess.check_output(f'module load JUBE; jube analyse {jube_bench_path} --id {jube_id}; jube result {jube_bench_path} --id {jube_id}', shell=True)
uuidgen_hash = subprocess.check_output('uuidgen', shell=True)[:-1].decode("utf-8")

results_source_path = os.path.join(jube_bench_path, jube_id.zfill(6), 'result', 'NEST_MAM.dat')
results_target_path = os.path.join('timing_results', f'{uuidgen_hash}.csv')
shutil.copy2(results_source_path, results_target_path)

dict_ = {
        uuidgen_hash: {
            'machine': 'JURECA-DC',
            'hyperthreading': False,
            'notes': [
                {'num vps per node': 128},
                {'MPI process per node': 4},
                {'threads per MPI proc': 32},
                {'nest': '2.14.1 with timers'},
                {'mam_state': 'Fig5'}
                ],
            'plot_name': 'scaling_2_14_1_Fig5',
            'reason': 'Benchmark comparison with NEST 3.',
            'where': [
                'jureca.fz-juelich.de',
                '/p/project/cjinb33/jinb3330/gitordner/BenchWork/jube_MAM/nest_2/000003'
                ]
            }
        }

with open('catalogue.yaml', 'r') as c:
    catalogue = yaml.safe_load(c)
    catalogue.update(dict_)

if overwrite:
    catalogue_fn = 'catalogue.yaml'
    with open('catalogue.yaml','w') as yamlfile:
        yaml.safe_dump(catalogue, yamlfile)
else:
    catalogue_fn = 'catalogue_new.yaml'
    with open('catalogue_new.yaml','w') as yamlfile:
        yaml.safe_dump(catalogue, yamlfile)

args = {
    'data_hash': uuidgen_hash,
    'data_path': './timing_results',
    'catalogue_path': catalogue_fn,
    'manually_set_plot_name': 'MAM node scaling',
    'x_axis': ['num_nodes'],
    'time_scaling': 1e3
}


# Instantiate class
B = bp.BenchPlot(**args)

# Plotting
widths = [1, 1]
heights = [3, 1]
fig = plt.figure(figsize=(12, 6), constrained_layout=True)
spec = gridspec.GridSpec(ncols=2, nrows=2, figure=fig, width_ratios=widths,
                         height_ratios=heights)

ax1 = fig.add_subplot(spec[:, 0])
ax2 = fig.add_subplot(spec[0, 1])
ax3 = fig.add_subplot(spec[1, 1])

B.plot_fractions(axis=ax1,
                 fill_variables=['wall_time_sim',
                                 'wall_time_create+wall_time_connect'],
                 interpolate=True,
                 step=None)
B.plot_main(quantities=['sim_factor', 'phase_total_factor'], axis=ax2)
B.plot_fractions(axis=ax3,
                 fill_variables=[
                     'frac_phase_communicate',
                     'frac_phase_update',
                     'frac_phase_deliver'])

ax1.set_xlabel('Number of Nodes')
ax1.set_ylabel('wall time [s]')
ax2.set_ylabel(r'real-time factor $T_{\mathrm{wall}}$'
               r'$T_{\mathrm{model}}$')
ax3.set_xlabel('Number of Nodes')

ax1.legend()
B.merge_legends(ax2, ax3)

plt.savefig(f'figures/{catalogue[uuidgen_hash]["plot_name"]}.pdf')
