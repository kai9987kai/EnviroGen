from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field, replace
from itertools import product
from pathlib import Path
from typing import Any, Iterable

from .entities import Bot, Obstacle, Plant
from .environment import Environment


@dataclass(frozen=True)
class ScenarioConfig:
    name: str
    width: int = 800
    height: int = 600
    seed: int | None = None
    steps: int = 200
    bot_count: int = 20
    plant_count: int = 80
    obstacle_count: int = 5
    bot_policy: str = "survival"
    bot_energy: float = 80.0
    bot_speed: float = 2.0
    bot_sight_radius: float = 80.0
    plant_energy: float = 25.0
    plant_growth_rate: float = 1.0
    obstacle_size: float = 40.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("scenario width and height must be positive")
        if self.steps < 0:
            raise ValueError("scenario steps must be non-negative")
        for name in ("bot_count", "plant_count", "obstacle_count"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be non-negative")


def create_environment(config: ScenarioConfig, seed: int | None = None) -> Environment:
    config.validate()
    env = Environment(width=config.width, height=config.height, seed=config.seed if seed is None else seed)
    rng = env.rng

    for _ in range(config.obstacle_count):
        env.add_obstacle(
            Obstacle(
                x=rng.uniform(0, max(0.0, config.width - config.obstacle_size)),
                y=rng.uniform(0, max(0.0, config.height - config.obstacle_size)),
                width=config.obstacle_size,
                height=config.obstacle_size,
            )
        )

    for _ in range(config.plant_count):
        env.add_plant(
            Plant(
                x=rng.uniform(5, config.width - 5),
                y=rng.uniform(5, config.height - 5),
                energy=config.plant_energy,
                max_energy=max(config.plant_energy, config.plant_energy * 2.0),
                growth_rate=config.plant_growth_rate,
            )
        )

    for _ in range(config.bot_count):
        env.add_bot(
            Bot(
                x=rng.uniform(5, config.width - 5),
                y=rng.uniform(5, config.height - 5),
                energy=config.bot_energy,
                speed=config.bot_speed,
                sight_radius=config.bot_sight_radius,
                policy=config.bot_policy,
            )
        )

    return env


def run_scenario(config: ScenarioConfig, dt: float = 1.0) -> list[dict[str, Any]]:
    env = create_environment(config)
    rows = [_with_scenario(config, env.metrics())]
    for _ in range(config.steps):
        rows.append(_with_scenario(config, env.step(dt=dt)))
    return rows


def run_batch(
    config: ScenarioConfig,
    seeds: Iterable[int],
    parameter_grid: dict[str, list[Any]] | None = None,
    dt: float = 1.0,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    grid = parameter_grid or {}
    keys = list(grid)
    combinations = product(*(grid[key] for key in keys)) if keys else [()]

    for values in combinations:
        overrides = dict(zip(keys, values))
        scenario = replace(config, **overrides)
        for seed in seeds:
            seeded = replace(scenario, seed=seed)
            metrics = run_scenario(seeded, dt=dt)[-1]
            metrics.update({"seed": seed, **overrides})
            rows.append(metrics)
    return rows


def export_metrics_csv(path: str | Path, rows: list[dict[str, Any]]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_metrics_json(path: str | Path, rows: list[dict[str, Any]]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def example_scenarios() -> dict[str, ScenarioConfig]:
    return {
        "stable_ecosystem": ScenarioConfig(
            name="stable_ecosystem",
            seed=7,
            bot_count=16,
            plant_count=120,
            plant_growth_rate=1.4,
            bot_energy=90,
            steps=300,
        ),
        "boom_bust_collapse": ScenarioConfig(
            name="boom_bust_collapse",
            seed=11,
            bot_count=40,
            plant_count=35,
            plant_growth_rate=0.35,
            bot_energy=110,
            steps=300,
        ),
        "trait_selection": ScenarioConfig(
            name="trait_selection",
            seed=23,
            bot_count=24,
            plant_count=90,
            plant_growth_rate=0.9,
            bot_speed=3.2,
            bot_sight_radius=110,
            steps=500,
        ),
    }


def _with_scenario(config: ScenarioConfig, row: dict[str, Any]) -> dict[str, Any]:
    return {"scenario": config.name, "seed": config.seed, **row}

