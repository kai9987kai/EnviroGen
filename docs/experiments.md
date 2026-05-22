# EnviroGen Experiments

EnviroGen scenarios are reproducible headless simulation runs. They are designed
for quick parameter sweeps before opening the Tkinter app.

```python
from envirogen import example_scenarios, run_batch, export_metrics_csv

scenario = example_scenarios()["stable_ecosystem"]
rows = run_batch(
    scenario,
    seeds=[1, 2, 3],
    parameter_grid={"plant_growth_rate": [0.5, 1.0, 1.5]},
)
export_metrics_csv("results/stable_growth_sweep.csv", rows)
```

Built-in scenarios:

| Scenario | Purpose |
| --- | --- |
| `stable_ecosystem` | Many plants with moderate bots; useful for steady-state behavior. |
| `boom_bust_collapse` | Too many bots and weak plant growth; demonstrates resource collapse. |
| `trait_selection` | Longer run with reproduction and mutation; tracks trait drift. |

Key metrics include population counts, plant biomass, total and average bot
energy, births, deaths, feedings, and average bot traits.

