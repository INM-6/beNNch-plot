<!--
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
-->

# beNNch-plot

This package provides standardized plotting routines. It is part of [beNNch](https://github.com/INM-6/beNNch), however, it can also be used in a standalone fashion.

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

Both commands install `beNNch-plot` as package such that it can be used anywhere on your system via `import bennchplot`.

## Using `beNNch-plot`

Conceptually, `beNNch-plot` adheres to a modular design philosophy. This means that arrangement of the created figure is not done internally but defineable on the surface level by the user. Concretely, this means that the user can provide their own `axis` objects, thereby retaining customization options such as setting titles and labels.
For measures that are used by default in [beNNch](https://github.com/INM-6/beNNch), default colors and labels are provided. This can be extended if desired.

### Examples

Examples of how to use `beNNch-plot` are provided in [`./examples`](./examples/). Here you can find examples for two models, the `microcircuit` and the `multi-area-model`. The necessary underlying performance results are given alongside.

#### microcircuit

The microcircuit serves as an example of a benchmark model that can be run across different numbers of virtual processes on a single node. After defining custom `axes`, `microcircuit.py` calls the two main plotting functions of `beNNch-plot`: `plot_main` for plotting simple line or error plots as `plot_fractions` to create a `fill_between`-style plot.

#### multi-area-model

In contrast to the microcircuit, the multi-area model showcases benchmarks across multiple number of nodes. While the basics are the same as for the microcircuit, an additional panel is created for showing the network construction time together with the state propagation time. Additionally, `multi-area-model_ram.py` gives a minimal example of how to plot other measurements than times.