from __future__ import annotations

from math import hypot
from random import Random
from typing import Callable, Iterable, TypeVar

from .entities import Bot, Entity, Obstacle, Plant
from .policies import resolve_policy
from .spatial import SpatialIndex

T = TypeVar("T", bound=Entity)


class Environment:
    """Headless simulation world for bots, plants, and obstacles."""

    def __init__(
        self,
        width: float = 800,
        height: float = 600,
        seed: int | None = None,
        cell_size: float = 50.0,
    ):
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        self.width = float(width)
        self.height = float(height)
        self.seed = seed
        self.rng = Random(seed)
        self.bots: list[Bot] = []
        self.plants: list[Plant] = []
        self.obstacles: list[Obstacle] = []
        self.time = 0.0
        self.step_count = 0
        self.births = 0
        self.deaths = 0
        self.feedings = 0
        self._next_id = 1
        self.spatial_index = SpatialIndex(cell_size=cell_size)

    @property
    def entities(self) -> list[Entity]:
        return [*self.bots, *self.plants, *self.obstacles]

    def add(self, entity: T) -> T:
        if entity.id is None:
            entity.id = self._next_id
            self._next_id += 1

        if isinstance(entity, Bot):
            self.bots.append(entity)
        elif isinstance(entity, Plant):
            self.plants.append(entity)
        elif isinstance(entity, Obstacle):
            self.obstacles.append(entity)
        else:
            raise TypeError(f"Unsupported entity type: {type(entity)!r}")

        self.clamp_entity(entity)
        self.rebuild_index()
        return entity

    def add_bot(self, bot: Bot | None = None, **kwargs) -> Bot:
        return self.add(bot if bot is not None else Bot(**kwargs))

    def add_plant(self, plant: Plant | None = None, **kwargs) -> Plant:
        return self.add(plant if plant is not None else Plant(**kwargs))

    def add_obstacle(self, obstacle: Obstacle | None = None, **kwargs) -> Obstacle:
        return self.add(obstacle if obstacle is not None else Obstacle(**kwargs))

    def rebuild_index(self) -> None:
        self.spatial_index.rebuild(self.entities)

    def clamp_position(self, entity: Entity, x: float, y: float) -> tuple[float, float]:
        if isinstance(entity, Obstacle):
            return (
                min(max(0.0, x), max(0.0, self.width - entity.width)),
                min(max(0.0, y), max(0.0, self.height - entity.height)),
            )
        return (
            min(max(entity.radius, x), self.width - entity.radius),
            min(max(entity.radius, y), self.height - entity.radius),
        )

    def clamp_entity(self, entity: Entity) -> None:
        entity.x, entity.y = self.clamp_position(entity, entity.x, entity.y)

    def collides_obstacle(self, x: float, y: float, radius: float) -> bool:
        return any(obstacle.intersects_circle(x, y, radius) for obstacle in self.obstacles)

    def can_move_to(self, entity: Entity, x: float, y: float) -> bool:
        if isinstance(entity, Obstacle):
            return True
        x, y = self.clamp_position(entity, x, y)
        return not self.collides_obstacle(x, y, entity.radius)

    def move_entity(self, entity: Entity, dx: float, dy: float) -> float:
        old_x, old_y = entity.x, entity.y
        target_x, target_y = self.clamp_position(entity, entity.x + dx, entity.y + dy)

        if self.can_move_to(entity, target_x, target_y):
            entity.x, entity.y = target_x, target_y
        elif self.can_move_to(entity, target_x, entity.y):
            entity.x = target_x
        elif self.can_move_to(entity, entity.x, target_y):
            entity.y = target_y

        return hypot(entity.x - old_x, entity.y - old_y)

    def nearby(self, entity: Entity, radius: float, kind: type[T] | None = None) -> list[T | Entity]:
        return [
            candidate
            for candidate in self.spatial_index.nearby(entity.x, entity.y, radius + entity.radius, kind)
            if candidate is not entity
        ]

    def nearest(
        self,
        entity: Entity,
        kind: type[T],
        radius: float | None = None,
        predicate: Callable[[T], bool] | None = None,
    ) -> T | None:
        if radius is None:
            candidates: Iterable[T] = self._entities_of_kind(kind)
        else:
            candidates = self.nearby(entity, radius, kind)

        nearest_entity: T | None = None
        nearest_distance = float("inf")
        for candidate in candidates:
            if candidate is entity or (predicate is not None and not predicate(candidate)):
                continue
            distance = self.distance_between(entity, candidate)
            if radius is not None and distance > radius:
                continue
            if distance < nearest_distance:
                nearest_entity = candidate
                nearest_distance = distance
        return nearest_entity

    def distance_between(self, first: Entity, second: Entity) -> float:
        if isinstance(second, Obstacle):
            closest_x = min(max(first.x, second.left), second.right)
            closest_y = min(max(first.y, second.top), second.bottom)
            return max(0.0, hypot(first.x - closest_x, first.y - closest_y) - first.radius)
        return max(0.0, first.distance_to(second) - first.radius - second.radius)

    def step(self, dt: float = 1.0) -> dict[str, float | int]:
        if dt <= 0:
            raise ValueError("dt must be positive")

        self.rebuild_index()
        for plant in self.plants:
            plant.grow(dt)

        newborns: list[Bot] = []
        for bot in list(self.bots):
            if not bot.alive:
                continue
            policy = resolve_policy(bot.policy)
            dx, dy = policy(bot, self)
            distance = self.move_entity(bot, dx * dt, dy * dt)
            bot.spend_energy(bot.metabolism * dt + distance * bot.move_cost)

            if bot.energy <= 0:
                bot.take_damage(bot.starvation_damage * dt)

            self._feed(bot, dt)

            if bot.reproduction_ready():
                bot.spend_energy(bot.reproduction_cost)
                child = bot.reproduce(self.rng)
                child.x, child.y = self.clamp_position(child, child.x, child.y)
                if self.collides_obstacle(child.x, child.y, child.radius):
                    child.x, child.y = bot.x, bot.y
                newborns.append(child)

        before = len(self.bots)
        self.bots = [bot for bot in self.bots if bot.alive]
        self.deaths += before - len(self.bots)

        for child in newborns:
            self.add(child)
            self.births += 1

        self.time += dt
        self.step_count += 1
        self.rebuild_index()
        return self.metrics()

    def run(self, steps: int, dt: float = 1.0) -> list[dict[str, float | int]]:
        if steps < 0:
            raise ValueError("steps must be non-negative")
        return [self.step(dt=dt) for _ in range(steps)]

    def metrics(self) -> dict[str, float | int]:
        bot_count = len(self.bots)
        plant_count = len(self.plants)
        total_bot_energy = sum(bot.energy for bot in self.bots)
        total_plant_energy = sum(plant.energy for plant in self.plants)
        return {
            "time": self.time,
            "step": self.step_count,
            "bots": bot_count,
            "plants": plant_count,
            "obstacles": len(self.obstacles),
            "bot_energy": total_bot_energy,
            "average_bot_energy": total_bot_energy / bot_count if bot_count else 0.0,
            "plant_biomass": total_plant_energy,
            "births": self.births,
            "deaths": self.deaths,
            "feedings": self.feedings,
            "average_speed": self._average("speed"),
            "average_sight_radius": self._average("sight_radius"),
            "average_metabolism": self._average("metabolism"),
        }

    def _feed(self, bot: Bot, dt: float) -> None:
        plant = self.nearest(
            bot,
            Plant,
            radius=bot.radius + max((plant.radius for plant in self.plants), default=0.0) + 2.0,
            predicate=lambda candidate: candidate.energy > 0,
        )
        if plant is None:
            return
        capacity = bot.max_energy - bot.energy
        if capacity <= 0:
            return
        taken = plant.harvest(min(bot.eat_rate * dt, capacity))
        if taken > 0:
            bot.receive_energy(taken)
            self.feedings += 1

    def _average(self, attr: str) -> float:
        if not self.bots:
            return 0.0
        return sum(float(getattr(bot, attr)) for bot in self.bots) / len(self.bots)

    def _entities_of_kind(self, kind: type[T]) -> list[T]:
        if kind is Bot:
            return list(self.bots)  # type: ignore[return-value]
        if kind is Plant:
            return list(self.plants)  # type: ignore[return-value]
        if kind is Obstacle:
            return list(self.obstacles)  # type: ignore[return-value]
        return [entity for entity in self.entities if isinstance(entity, kind)]
