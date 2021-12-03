import benchplot as bp
from matplotlib import pyplot as plt


"""
define what to plot:
- data_file:
    Path to .csv file containing benchmarking measurements.
- x_axis:
    Giving a list of strings corresponding to the main scaling
    variable, typically 'num_nodes' or 'num_nvp'.
- time_scaling:
    Quotient between unit time of timing measurement and
    simulation. Usually, the former is given in s while
    the latter is given in ms. 
"""
args = {
    'data_file': '45011f6d-c3c2-4f2c-b884-af04e9edc5b9.csv',
    'x_axis': ['num_nodes'],
    'time_scaling': 1e3
}

# Instantiate class
B = bp.BenchPlot(**args)

# Figure layout
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 6))

# Add plot
B.plot_main(quantities=['total_memory'], axis=ax,
            error=True, fmt='-')

# Set labels, limits etc.
ax.set_xlabel('Number of nodes')
ax.set_ylabel('RAM [B]')
ax.legend()

# Save figure
plt.savefig('ram_usage.pdf')
