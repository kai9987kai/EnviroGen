import tkinter as tk
from .bot import Bot
from .obstacle import Obstacle
from .plant import Plant

class Environment:
    def __init__(self, window: tk.Tk, canvas: tk.Canvas):
        self.window = window
        self.canvas = canvas
        self.bots = []
        self.obstacles = []
        self.plants = []

    def add_bot(self, bot: Bot):
        self.bots.append(bot)

    def add_obstacle(self, obstacle: Obstacle):
        self.obstacles.append(obstacle)

    def add_plant(self, plant: Plant):
        self.plants.append(plant)

    def update(self):
        for bot in self.bots:
            bot.move()
        self.window.after(100, self.update)  # Schedule the next update in 100 ms

    def run(self):
        self.update()
        self.window.mainloop()
