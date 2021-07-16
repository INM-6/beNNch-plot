import benchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


args = {
    'data_hash': 'a9d9b91e-e3da-4f91-b9c2-2f8c60347c53',
    'data_path': '../../timing_results',
    'catalogue_path': '../../catalogue.yaml',
    'x_axis': ['num_nodes'],
    'time_scaling': 1e3
}

# Instantiate class
B = bp.BenchPlot(**args)

# Plotting
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 6))

B.plot_main(quantities=['total_memory'], axis=ax,
            error=True)

ax.set_xlabel('Number of Nodes')
ax.set_ylabel('RAM [B]')

ax.legend()
plt.savefig('ram_3.0_Fig5_JUSUF.pdf')
