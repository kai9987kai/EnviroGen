from __future__ import annotations

import webbrowser
from typing import Literal

from .entities import Bot, Entity, Obstacle, Plant
from .environment import Environment
from .resources import RESOURCE_CATALOG, Resource, resources_by_category

ToolName = Literal["bot", "plant", "obstacle", "inspect"]


class EnviroGenApp:
    """Tkinter demo interface for an EnviroGen environment."""

    def __init__(
        self,
        env: Environment | None = None,
        *,
        width: int = 800,
        height: int = 600,
        tick_ms: int = 50,
    ):
        self.env = env or Environment(width=width, height=height)
        self.tick_ms = tick_ms
        self.running = False
        self.tool: ToolName = "inspect"
        self.speed = 1
        self.selected: Entity | None = None
        self._items: dict[int, int] = {}
        self._tk = None
        self.root = None
        self.canvas = None
        self.status_var = None
        self.inspector_var = None
        self.speed_var = None
        self.resource_list = None
        self._resources: list[Resource] = []

    def run(self) -> None:
        self._ensure_ui()
        self._render()
        self.root.mainloop()

    def _ensure_ui(self) -> None:
        if self.root is not None:
            return
        import tkinter as tk
        from tkinter import ttk

        self._tk = tk
        self.root = tk.Tk()
        self.root.title("EnviroGen")

        main = ttk.Frame(self.root, padding=8)
        main.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        toolbar = ttk.Frame(main)
        toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        ttk.Button(toolbar, text="Start", command=self.start).pack(side="left")
        ttk.Button(toolbar, text="Pause", command=self.pause).pack(side="left", padx=(4, 0))
        ttk.Button(toolbar, text="Step", command=self.step_once).pack(side="left", padx=(4, 0))
        ttk.Button(toolbar, text="Reset", command=self.reset).pack(side="left", padx=(4, 12))

        for label, tool in (("Inspect", "inspect"), ("Bot", "bot"), ("Plant", "plant"), ("Obstacle", "obstacle")):
            ttk.Button(toolbar, text=label, command=lambda value=tool: self.set_tool(value)).pack(side="left", padx=(0, 4))

        self.speed_var = tk.IntVar(value=self.speed)
        ttk.Label(toolbar, text="Speed").pack(side="left", padx=(12, 4))
        ttk.Scale(toolbar, from_=1, to=20, variable=self.speed_var, command=self._set_speed).pack(side="left")

        self.status_var = tk.StringVar()
        ttk.Label(toolbar, textvariable=self.status_var).pack(side="right")

        self.canvas = tk.Canvas(main, width=self.env.width, height=self.env.height, bg="#f6f7f2", highlightthickness=1)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        side = ttk.Notebook(main)
        side.grid(row=1, column=1, sticky="ns", padx=(8, 0))

        inspect_tab = ttk.Frame(side, padding=8)
        resources_tab = ttk.Frame(side, padding=8)
        side.add(inspect_tab, text="Inspect")
        side.add(resources_tab, text="Resources")

        self.inspector_var = tk.StringVar(value="No entity selected")
        ttk.Label(inspect_tab, textvariable=self.inspector_var, justify="left", width=34).pack(anchor="nw")

        self.resource_list = tk.Listbox(resources_tab, width=46, height=24)
        self.resource_list.pack(fill="both", expand=True)
        ttk.Button(resources_tab, text="Open", command=self.open_selected_resource).pack(anchor="e", pady=(8, 0))
        self._load_resources()

    def start(self) -> None:
        self._ensure_ui()
        if not self.running:
            self.running = True
            self._schedule()

    def pause(self) -> None:
        self.running = False

    def reset(self) -> None:
        self.pause()
        seed = self.env.seed
        width, height = self.env.width, self.env.height
        self.env = Environment(width=width, height=height, seed=seed)
        self.selected = None
        self._items.clear()
        self._render()

    def step_once(self) -> None:
        self._ensure_ui()
        for _ in range(max(1, self.speed)):
            self.env.step()
        self._render()

    def set_tool(self, tool: ToolName) -> None:
        self.tool = tool

    def open_selected_resource(self) -> None:
        if self.resource_list is None:
            return
        selection = self.resource_list.curselection()
        if not selection:
            return
        resource = self._resources[selection[0]]
        webbrowser.open(resource.url)

    def _schedule(self) -> None:
        if not self.running or self.root is None:
            return
        self.step_once()
        self.root.after(self.tick_ms, self._schedule)

    def _set_speed(self, _value: str) -> None:
        if self.speed_var is not None:
            self.speed = int(float(self.speed_var.get()))

    def _on_canvas_click(self, event) -> None:
        if self.tool == "bot":
            self.env.add_bot(x=event.x, y=event.y)
        elif self.tool == "plant":
            self.env.add_plant(x=event.x, y=event.y)
        elif self.tool == "obstacle":
            self.env.add_obstacle(x=event.x - 20, y=event.y - 20)
        else:
            self.selected = self._pick(event.x, event.y)
        self._render()

    def _pick(self, x: float, y: float) -> Entity | None:
        probe = Plant(x=x, y=y, radius=1)
        nearest = None
        nearest_distance = 12.0
        for entity in self.env.entities:
            distance = self.env.distance_between(probe, entity)
            if distance < nearest_distance:
                nearest = entity
                nearest_distance = distance
        return nearest

    def _load_resources(self) -> None:
        if self.resource_list is None:
            return
        self.resource_list.delete(0, "end")
        self._resources.clear()
        for category, resources in resources_by_category().items():
            for resource in resources:
                self._resources.append(resource)
                self.resource_list.insert("end", f"{category}: {resource.title}")

    def _render(self) -> None:
        if self.canvas is None:
            return
        live_ids = {entity.id for entity in self.env.entities}
        for entity_id, item in list(self._items.items()):
            if entity_id not in live_ids:
                self.canvas.delete(item)
                del self._items[entity_id]

        for obstacle in self.env.obstacles:
            self._render_obstacle(obstacle)
        for plant in self.env.plants:
            self._render_plant(plant)
        for bot in self.env.bots:
            self._render_bot(bot)

        self._update_labels()

    def _render_bot(self, bot: Bot) -> None:
        fill = "#d94841" if bot.energy > bot.max_energy * 0.35 else "#8f2d24"
        outline = "#111111" if bot is self.selected else ""
        self._oval(bot, fill=fill, outline=outline)

    def _render_plant(self, plant: Plant) -> None:
        ratio = plant.energy / plant.max_energy if plant.max_energy else 0.0
        fill = "#2f9e44" if ratio > 0.4 else "#a4c639"
        outline = "#111111" if plant is self.selected else ""
        self._oval(plant, fill=fill, outline=outline)

    def _render_obstacle(self, obstacle: Obstacle) -> None:
        if obstacle.id not in self._items:
            self._items[obstacle.id] = self.canvas.create_rectangle(
                obstacle.left,
                obstacle.top,
                obstacle.right,
                obstacle.bottom,
                fill="#4a6fa5",
                outline="#111111" if obstacle is self.selected else "",
            )
        else:
            item = self._items[obstacle.id]
            self.canvas.coords(item, obstacle.left, obstacle.top, obstacle.right, obstacle.bottom)
            self.canvas.itemconfigure(item, outline="#111111" if obstacle is self.selected else "")

    def _oval(self, entity: Entity, *, fill: str, outline: str) -> None:
        assert self.canvas is not None
        x0 = entity.x - entity.radius
        y0 = entity.y - entity.radius
        x1 = entity.x + entity.radius
        y1 = entity.y + entity.radius
        if entity.id not in self._items:
            self._items[entity.id] = self.canvas.create_oval(x0, y0, x1, y1, fill=fill, outline=outline)
        else:
            item = self._items[entity.id]
            self.canvas.coords(item, x0, y0, x1, y1)
            self.canvas.itemconfigure(item, fill=fill, outline=outline)

    def _update_labels(self) -> None:
        if self.status_var is not None:
            metrics = self.env.metrics()
            self.status_var.set(
                f"step {metrics['step']} | bots {metrics['bots']} | plants {metrics['plants']} | births {metrics['births']} | deaths {metrics['deaths']}"
            )
        if self.inspector_var is not None:
            if self.selected is None:
                self.inspector_var.set("No entity selected")
            else:
                details = "\n".join(f"{key}: {value}" for key, value in self.selected.as_dict().items())
                self.inspector_var.set(details)


__all__ = ["EnviroGenApp", "RESOURCE_CATALOG"]

