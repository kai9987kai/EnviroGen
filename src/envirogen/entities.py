from __future__ import annotations

from dataclasses import dataclass, field
from math import hypot, isfinite
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    import random

    from .environment import Environment

Policy = Callable[["Bot", "Environment"], tuple[float, float]]


@dataclass
class Entity:
    """Base simulation object with a position in continuous 2D space."""

    x: float
    y: float
    radius: float = 0.0
    id: int | None = field(default=None, init=False, compare=False)

    @property
    def kind(self) -> str:
        return self.__class__.__name__.lower()

    def distance_to(self, other: "Entity") -> float:
        return hypot(self.x - other.x, self.y - other.y)

    def __post_init__(self) -> None:
        if not isfinite(self.x) or not isfinite(self.y):
            raise ValueError("entity positions must be finite numbers")
        if self.radius < 0:
            raise ValueError("entity radius must be non-negative")

    def as_dict(self) -> dict[str, float | int | str | None]:
        return {
            "id": self.id,
            "kind": self.kind,
            "x": self.x,
            "y": self.y,
            "radius": self.radius,
        }


@dataclass
class Plant(Entity):
    """Regenerating edible resource."""

    radius: float = 5.0
    energy: float = 25.0
    max_energy: float = 50.0
    growth_rate: float = 1.0

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.max_energy <= 0:
            raise ValueError("plant max_energy must be positive")
        if self.growth_rate < 0:
            raise ValueError("plant growth_rate must be non-negative")
        self.energy = min(self.max_energy, max(0.0, self.energy))

    @property
    def edible(self) -> bool:
        return self.energy > 0

    def grow(self, dt: float = 1.0) -> None:
        self.energy = min(self.max_energy, self.energy + self.growth_rate * dt)

    def harvest(self, amount: float) -> float:
        taken = max(0.0, min(self.energy, amount))
        self.energy -= taken
        return taken

    def as_dict(self) -> dict[str, float | int | str | None]:
        data = super().as_dict()
        data.update(
            {
                "energy": self.energy,
                "max_energy": self.max_energy,
                "growth_rate": self.growth_rate,
            }
        )
        return data


@dataclass
class Obstacle(Entity):
    """Axis-aligned rectangular barrier."""

    width: float = 40.0
    height: float = 40.0

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.width <= 0 or self.height <= 0:
            raise ValueError("obstacle width and height must be positive")

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2.0

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2.0

    def intersects_circle(self, x: float, y: float, radius: float) -> bool:
        closest_x = min(max(x, self.left), self.right)
        closest_y = min(max(y, self.top), self.bottom)
        return hypot(x - closest_x, y - closest_y) <= radius

    def as_dict(self) -> dict[str, float | int | str | None]:
        data = super().as_dict()
        data.update({"width": self.width, "height": self.height})
        return data


@dataclass
class Bot(Entity):
    """Mobile agent with local sensing, energy, health, and heritable traits."""

    radius: float = 5.0
    health: float = 100.0
    energy: float = 50.0
    max_energy: float = 150.0
    speed: float = 2.0
    sight_radius: float = 80.0
    metabolism: float = 0.4
    move_cost: float = 0.05
    eat_rate: float = 15.0
    starvation_damage: float = 4.0
    reproduction_threshold: float = 120.0
    reproduction_cost: float = 60.0
    mutation_rate: float = 0.08
    policy: str | Policy | None = "survival"

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.max_energy <= 0:
            raise ValueError("bot max_energy must be positive")
        if self.speed < 0:
            raise ValueError("bot speed must be non-negative")
        if self.sight_radius < 0:
            raise ValueError("bot sight_radius must be non-negative")
        if self.metabolism < 0 or self.move_cost < 0 or self.eat_rate < 0:
            raise ValueError("bot energy rates must be non-negative")
        if self.reproduction_threshold < 0 or self.reproduction_cost < 0:
            raise ValueError("bot reproduction values must be non-negative")
        if self.mutation_rate < 0:
            raise ValueError("bot mutation_rate must be non-negative")
        self.health = max(0.0, self.health)
        self.energy = min(self.max_energy, max(0.0, self.energy))

    @property
    def alive(self) -> bool:
        return self.health > 0

    def take_damage(self, amount: float) -> None:
        self.health = max(0.0, self.health - max(0.0, amount))

    def spend_energy(self, amount: float) -> None:
        self.energy = max(0.0, self.energy - max(0.0, amount))

    def receive_energy(self, amount: float) -> float:
        gained = max(0.0, min(amount, self.max_energy - self.energy))
        self.energy += gained
        return gained

    def reproduction_ready(self) -> bool:
        return self.alive and self.energy >= self.reproduction_threshold

    def reproduce(self, rng: "random.Random") -> "Bot":
        def mutate(value: float, low: float, high: float) -> float:
            if self.mutation_rate <= 0:
                return min(high, max(low, value))
            factor = 1.0 + rng.uniform(-self.mutation_rate, self.mutation_rate)
            return min(high, max(low, value * factor))

        return Bot(
            x=self.x + rng.uniform(-self.radius * 2.0, self.radius * 2.0),
            y=self.y + rng.uniform(-self.radius * 2.0, self.radius * 2.0),
            radius=self.radius,
            health=self.health,
            energy=max(5.0, self.reproduction_cost * 0.5),
            max_energy=self.max_energy,
            speed=mutate(self.speed, 0.1, 20.0),
            sight_radius=mutate(self.sight_radius, 5.0, 500.0),
            metabolism=mutate(self.metabolism, 0.01, 20.0),
            move_cost=self.move_cost,
            eat_rate=self.eat_rate,
            starvation_damage=self.starvation_damage,
            reproduction_threshold=self.reproduction_threshold,
            reproduction_cost=self.reproduction_cost,
            mutation_rate=self.mutation_rate,
            policy=self.policy,
        )

    def as_dict(self) -> dict[str, float | int | str | None]:
        data = super().as_dict()
        data.update(
            {
                "health": self.health,
                "energy": self.energy,
                "max_energy": self.max_energy,
                "speed": self.speed,
                "sight_radius": self.sight_radius,
                "metabolism": self.metabolism,
                "reproduction_threshold": self.reproduction_threshold,
            }
        )
        return data
