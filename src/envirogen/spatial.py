from __future__ import annotations

from collections import defaultdict
from math import floor, hypot
from typing import Iterable, TypeVar

from .entities import Entity, Obstacle

T = TypeVar("T", bound=Entity)


class SpatialIndex:
    """Small uniform-grid spatial index for nearby entity lookups."""

    def __init__(self, cell_size: float = 50.0):
        if cell_size <= 0:
            raise ValueError("cell_size must be positive")
        self.cell_size = cell_size
        self._buckets: dict[tuple[int, int], list[Entity]] = defaultdict(list)

    def clear(self) -> None:
        self._buckets.clear()

    def rebuild(self, entities: Iterable[Entity]) -> None:
        self.clear()
        for entity in entities:
            self.insert(entity)

    def insert(self, entity: Entity) -> None:
        for cell in self._cells_for(entity):
            self._buckets[cell].append(entity)

    def nearby(self, x: float, y: float, radius: float, kind: type[T] | None = None) -> list[T | Entity]:
        min_cell_x = floor((x - radius) / self.cell_size)
        max_cell_x = floor((x + radius) / self.cell_size)
        min_cell_y = floor((y - radius) / self.cell_size)
        max_cell_y = floor((y + radius) / self.cell_size)
        found: list[T | Entity] = []
        seen: set[int] = set()

        for cx in range(min_cell_x, max_cell_x + 1):
            for cy in range(min_cell_y, max_cell_y + 1):
                for entity in self._buckets.get((cx, cy), []):
                    if id(entity) in seen:
                        continue
                    if kind is not None and not isinstance(entity, kind):
                        continue
                    if _within(entity, x, y, radius):
                        found.append(entity)
                        seen.add(id(entity))
        return found

    def _cells_for(self, entity: Entity) -> list[tuple[int, int]]:
        if isinstance(entity, Obstacle):
            left = entity.left
            right = entity.right
            top = entity.top
            bottom = entity.bottom
        else:
            left = entity.x - entity.radius
            right = entity.x + entity.radius
            top = entity.y - entity.radius
            bottom = entity.y + entity.radius

        min_cell_x = floor(left / self.cell_size)
        max_cell_x = floor(right / self.cell_size)
        min_cell_y = floor(top / self.cell_size)
        max_cell_y = floor(bottom / self.cell_size)
        return [
            (cx, cy)
            for cx in range(min_cell_x, max_cell_x + 1)
            for cy in range(min_cell_y, max_cell_y + 1)
        ]


def _within(entity: Entity, x: float, y: float, radius: float) -> bool:
    if isinstance(entity, Obstacle):
        return entity.intersects_circle(x, y, radius)
    return hypot(entity.x - x, entity.y - y) <= radius + entity.radius

