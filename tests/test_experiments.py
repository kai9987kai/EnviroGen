from __future__ import annotations

import json

import pytest

from envirogen import (
    ScenarioConfig,
    example_scenarios,
    export_metrics_csv,
    export_metrics_json,
    run_batch,
    run_scenario,
)


def test_same_scenario_and_seed_are_deterministic() -> None:
    config = ScenarioConfig(name="deterministic", seed=42, steps=20, bot_count=5, plant_count=20, obstacle_count=2)

    assert run_scenario(config) == run_scenario(config)


def test_invalid_scenario_fails_early() -> None:
    with pytest.raises(ValueError):
        ScenarioConfig(name="bad", width=0).validate()


def test_batch_runs_isolate_parameter_and_seed_combinations() -> None:
    config = ScenarioConfig(name="batch", steps=5, bot_count=3, plant_count=5, obstacle_count=0)

    rows = run_batch(config, seeds=[1, 2], parameter_grid={"plant_growth_rate": [0.5, 1.0]})

    assert len(rows) == 4
    assert {row["seed"] for row in rows} == {1, 2}
    assert {row["plant_growth_rate"] for row in rows} == {0.5, 1.0}
    assert all(row["scenario"] == "batch" for row in rows)


def test_metric_exports_create_csv_and_json(tmp_path) -> None:
    rows = run_scenario(ScenarioConfig(name="export", seed=3, steps=2, bot_count=1, plant_count=1, obstacle_count=0))
    csv_path = tmp_path / "metrics.csv"
    json_path = tmp_path / "metrics.json"

    export_metrics_csv(csv_path, rows)
    export_metrics_json(json_path, rows)

    assert csv_path.read_text(encoding="utf-8").startswith("average_bot_energy")
    assert json.loads(json_path.read_text(encoding="utf-8")) == rows


def test_example_scenarios_cover_expected_dynamics() -> None:
    scenarios = example_scenarios()

    assert {"stable_ecosystem", "boom_bust_collapse", "trait_selection"} <= set(scenarios)

