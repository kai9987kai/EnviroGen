# EnviroGen

EnviroGen is a lightweight Python agent-based ecosystem simulator. It models
bots, plants, obstacles, local sensing, energy, plant growth, feeding, death,
reproduction, mutation, metrics, and repeatable experiments.

The simulation core is headless and deterministic with a seed. Tkinter is used
only for the optional demo app.

## Install

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
pytest
```

## Quickstart

```python
from envirogen import Bot, Environment, Obstacle, Plant

env = Environment(width=800, height=600, seed=42)

for index in range(12):
    env.add_bot(Bot(x=80 + index * 10, y=80, policy="survival"))

for index in range(60):
    env.add_plant(Plant(x=40 + index * 10, y=300, growth_rate=1.2))

env.add_obstacle(Obstacle(x=350, y=220, width=90, height=70))

history = env.run(steps=250)
print(history[-1])
```

## Tkinter App

```python
from envirogen import EnviroGenApp, Environment

app = EnviroGenApp(Environment(width=800, height=600, seed=7))
app.run()
```

The app includes start, pause, single-step, reset, speed control, click-to-place
tools, entity inspection, live counters, and a Resources panel that opens
external learning links.

## Experiments

```python
from envirogen import example_scenarios, export_metrics_csv, run_batch

scenario = example_scenarios()["stable_ecosystem"]
rows = run_batch(
    scenario,
    seeds=[1, 2, 3],
    parameter_grid={"plant_growth_rate": [0.5, 1.0, 1.5]},
)
export_metrics_csv("results/stable_growth_sweep.csv", rows)
```

See [docs/experiments.md](docs/experiments.md) for the built-in scenarios and
metrics.

## Resource Catalog

See [docs/resources.md](docs/resources.md) for curated videos, courses,
tutorials, examples, and research references covering agent-based modeling,
Mesa, NetLogo, artificial life, ecology simulation, experiments, optimization,
and visualization. EnviroGen links to external resources; it does not bundle
video assets.

## Release Security

The previous publish workflow contained a hard-coded PyPI credential expression.
That credential must be revoked in PyPI outside this repository. The workflow now
uses PyPI trusted publishing via GitHub Actions OIDC instead of storing a token in
the repo.

