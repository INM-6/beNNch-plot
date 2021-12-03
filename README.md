# benchplot

This package provides standardized plotting routines. It is part of the [NEST Benchmarking Framework](https://github.com/INM-6/nest_benchmarking_framework), however, it can also be used in a standalone fashion.

It is designed to work with performance benchmarking results stored in `.csv` files that adhere to a common naming convention.

## Installation

### pip

On the top level, run

```bash
pip install .
```

Alternatively, if you want to make changes on the fly (e.g. change plotting parameters), execute

```bash
pip install -e .
```

Both commands install `benchplot` as package such that it can be used anywhere on your system.

## Using `benchplot`

Conceptually, `benchplot` adheres to a modular design philosophy. This means that arrangement of the created figure is not done internally but defineable on the surface level by the user. Concretely, this means that the user can provide their own `axis` objects, thereby retaining customization options such as setting titles and labels.
For measures that are used by default in the [NEST Benchmarking Framework](https://github.com/INM-6/nest_benchmarking_framework), default colors and labels are provided. This can be extended if desired.

### Examples

Examples of how to use `benchplot` are provided in [`./examples`](https://github.com/INM-6/benchplot/tree/main/examples). Here you can find examples for two models, the `microcircuit` and the `multi-area-model`. The necessary underlying performance results are given alongside.

#### microcircuit

The microcircuit serves as an example of a benchmark model that can be run across different numbers of virtual processes on a single node. After defining custom `axes`, `microcircuit.py` calls the two main plotting functions of `benchplot`: `plot_main` for plotting simple line or error plots as `plot_fractions` to create a `fill_between`-style plot.

#### multi-area-model

In contrast to the microcircuit, the multi-area model showcases benchmarks across multiple number of nodes. While the basics are the same as for the microcircuit, an additional panel is created for showing the network construction time together with the state propagation time. Additionally, `multi-area-model_ram.py` gives a minimal example of how to plot other measurements than times.