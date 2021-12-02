import benchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


args = {
    'data_file': '45011f6d-c3c2-4f2c-b884-af04e9edc5b9.csv',
    'x_axis': ['num_nodes'],
    'time_scaling': 1e3
}

# Instantiate class
B = bp.BenchPlot(**args)

# Plotting
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 6))

B.plot_main(quantities=['total_memory'], axis=ax,
            error=True, fmt='-')

ax.set_xlabel('Number of nodes')
ax.set_ylabel('RAM [B]')

ax.legend()
plt.savefig('ram_usage.pdf')
