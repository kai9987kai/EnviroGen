from __future__ import annotations

from math import atan2, cos, hypot, sin, tau
from typing import Callable

from .entities import Bot, Obstacle, Plant

Policy = Callable[[Bot, "Environment"], tuple[float, float]]


def _limited(dx: float, dy: float, distance: float) -> tuple[float, float]:
    length = hypot(dx, dy)
    if length == 0:
        return 0.0, 0.0
    scale = min(distance, length) / length
    return dx * scale, dy * scale


def _toward(bot: Bot, x: float, y: float, distance: float) -> tuple[float, float]:
    return _limited(x - bot.x, y - bot.y, distance)


def random_walk_policy(bot: Bot, env: "Environment") -> tuple[float, float]:
    angle = env.rng.random() * tau
    return cos(angle) * bot.speed, sin(angle) * bot.speed


def seek_nearest_plant_policy(bot: Bot, env: "Environment") -> tuple[float, float]:
    plant = env.nearest(
        bot,
        Plant,
        radius=bot.sight_radius,
        predicate=lambda candidate: candidate.energy > 0,
    )
    if plant is None:
        return random_walk_policy(bot, env)
    return _toward(bot, plant.x, plant.y, bot.speed)


def avoid_obstacle_policy(bot: Bot, env: "Environment") -> tuple[float, float]:
    obstacle = env.nearest(bot, Obstacle, radius=bot.sight_radius)
    if obstacle is None:
        return random_walk_policy(bot, env)

    dx = bot.x - obstacle.center_x
    dy = bot.y - obstacle.center_y
    if dx == 0 and dy == 0:
        angle = env.rng.random() * tau
        dx, dy = cos(angle), sin(angle)
    return _limited(dx, dy, bot.speed)


def survival_policy(bot: Bot, env: "Environment") -> tuple[float, float]:
    obstacle = env.nearest(bot, Obstacle, radius=max(bot.radius * 4.0, bot.sight_radius / 3.0))
    if obstacle is not None and obstacle.intersects_circle(bot.x, bot.y, bot.radius * 4.0):
        return avoid_obstacle_policy(bot, env)

    if bot.energy < bot.max_energy * 0.85:
        return seek_nearest_plant_policy(bot, env)

    # Add small wandering pressure so well-fed populations still explore.
    return random_walk_policy(bot, env)


POLICIES: dict[str, Policy] = {
    "random": random_walk_policy,
    "random_walk": random_walk_policy,
    "seek_plant": seek_nearest_plant_policy,
    "seek_nearest_plant": seek_nearest_plant_policy,
    "avoid_obstacle": avoid_obstacle_policy,
    "survival": survival_policy,
}


def resolve_policy(policy: str | Policy | None) -> Policy:
    if policy is None:
        return lambda bot, env: (0.0, 0.0)
    if callable(policy):
        return policy
    try:
        return POLICIES[policy]
    except KeyError as exc:
        options = ", ".join(sorted(POLICIES))
        raise ValueError(f"Unknown bot policy {policy!r}; expected one of: {options}") from exc


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .environment import Environment

