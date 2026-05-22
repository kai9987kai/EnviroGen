from __future__ import annotations

import pytest

from envirogen import Bot, Environment, Obstacle, Plant


def test_bot_moves_toward_nearest_plant() -> None:
    env = Environment(width=100, height=100, seed=4)
    bot = env.add_bot(
        Bot(
            x=10,
            y=10,
            speed=5,
            metabolism=0,
            move_cost=0,
            policy="seek_nearest_plant",
        )
    )
    env.add_plant(Plant(x=40, y=10, energy=20, growth_rate=0))

    env.step()

    assert bot.x > 10
    assert bot.y == pytest.approx(10)


def test_bounds_clamp_bot_position() -> None:
    env = Environment(width=30, height=30, seed=1)
    bot = env.add_bot(Bot(x=25, y=25, radius=5, speed=20, metabolism=0, move_cost=0, policy=lambda _bot, _env: (20, 20)))

    env.step()

    assert bot.x <= 25
    assert bot.y <= 25


def test_obstacle_blocks_movement() -> None:
    env = Environment(width=100, height=100, seed=1)
    bot = env.add_bot(Bot(x=20, y=50, radius=5, speed=50, metabolism=0, move_cost=0, policy=lambda _bot, _env: (40, 0)))
    env.add_obstacle(Obstacle(x=35, y=40, width=20, height=20))

    env.step()

    assert bot.x == pytest.approx(20)
    assert bot.y == pytest.approx(50)


def test_plant_grows_to_max_energy() -> None:
    plant = Plant(x=1, y=1, energy=5, max_energy=10, growth_rate=3)

    plant.grow(dt=3)

    assert plant.energy == 10


def test_bot_eats_plant_atomically() -> None:
    env = Environment(width=100, height=100, seed=1)
    bot = env.add_bot(Bot(x=20, y=20, energy=10, metabolism=0, move_cost=0, eat_rate=8, policy=None))
    plant = env.add_plant(Plant(x=20, y=20, energy=20, growth_rate=0))

    env.step()

    assert bot.energy == pytest.approx(18)
    assert plant.energy == pytest.approx(12)
    assert env.metrics()["feedings"] == 1


def test_starvation_removes_dead_bot() -> None:
    env = Environment(width=100, height=100, seed=1)
    env.add_bot(Bot(x=20, y=20, energy=0, health=4, metabolism=0, starvation_damage=4, policy=None))

    metrics = env.step()

    assert metrics["bots"] == 0
    assert metrics["deaths"] == 1


def test_reproduction_creates_mutated_child_within_bounds() -> None:
    env = Environment(width=100, height=100, seed=1)
    env.add_bot(
        Bot(
            x=50,
            y=50,
            energy=130,
            metabolism=0,
            move_cost=0,
            reproduction_threshold=120,
            reproduction_cost=60,
            mutation_rate=1.0,
            policy=None,
        )
    )

    metrics = env.step()

    assert metrics["bots"] == 2
    assert metrics["births"] == 1
    child = env.bots[1]
    for bot in env.bots:
        assert 0.1 <= bot.speed <= 20
        assert 5 <= bot.sight_radius <= 500
        assert bot.radius <= bot.x <= env.width - bot.radius
        assert bot.radius <= bot.y <= env.height - bot.radius
    assert 0.01 <= child.metabolism <= 20


def test_invalid_entity_values_fail_fast() -> None:
    with pytest.raises(ValueError):
        Plant(x=0, y=0, max_energy=0)
    with pytest.raises(ValueError):
        Obstacle(x=0, y=0, width=0)
    with pytest.raises(ValueError):
        Bot(x=0, y=0, speed=-1)
