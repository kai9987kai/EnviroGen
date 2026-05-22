from __future__ import annotations

from random import Random

from envirogen import Bot, Environment, Plant


def test_spatial_index_matches_brute_force_nearby_queries() -> None:
    env = Environment(width=500, height=500, seed=10, cell_size=25)
    rng = Random(10)
    probe = env.add_bot(Bot(x=250, y=250, policy=None))

    for _ in range(200):
        env.add_plant(Plant(x=rng.uniform(0, 500), y=rng.uniform(0, 500)))

    indexed = {plant.id for plant in env.nearby(probe, radius=100, kind=Plant)}
    brute = {
        plant.id
        for plant in env.plants
        if probe.distance_to(plant) <= 100 + probe.radius + plant.radius
    }

    assert indexed == brute
    assert probe.id not in indexed


def test_spatial_index_is_rebuilt_after_movement() -> None:
    env = Environment(width=200, height=200, seed=1, cell_size=20)
    bot = env.add_bot(Bot(x=10, y=10, speed=100, metabolism=0, move_cost=0, policy=lambda _bot, _env: (100, 0)))

    env.step()

    assert bot in env.spatial_index.nearby(bot.x, bot.y, radius=1, kind=Bot)

