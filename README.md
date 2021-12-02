# benchplot

This package provides standardized plotting routines. It is part of the [NEST Benchmarking Framework](https://github.com/INM-6/nest_benchmarking_framework), however, it can also be used in a stand alone fashion.

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

Examples of how to use `benchplot` are provided in [`./examples`](https://github.com/INM-6/benchplot/tree/main/examples). Here you can find examples for two models, the `microcircuit` and the `multi-area-model`. The necessary underlying performance results are given alongside.

Conceptually, `benchplot` adheres to a modular design philosophy. This means that arrangement of the created figure is not done internally but defineable on the surface level by the user. Concretely, this means that the user can provide their own `axis` objects, thereby retaining customization options such as setting titles and labels.
For measures that are used by default in the [NEST Benchmarking Framework](https://github.com/INM-6/nest_benchmarking_framework), default colors and labels are provided. This can be extended if desired.
