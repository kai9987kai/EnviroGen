# EnviroGen Python Package Documentation

## Overview

EnviroGen is a Python package that allows users to create 2D environments with bots, obstacles, and plants using a Tkinter canvas. The bots can move around the environment, interact with obstacles and plants, and have health attributes. Obstacles have a size attribute and plants have an energy attribute and can grow.

## Installation

To install the EnviroGen package, use pip:

```
pip install envirogen
```

## Usage

Here's a basic example of how to use the EnviroGen package:

```python
import tkinter as tk
from envirogen import Environment, Bot, Obstacle, Plant

# Create a Tkinter window and canvas
window = tk.Tk()
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()

# Create an environment
env = Environment(window, canvas)

# Add bots, obstacles, and plants to the environment
for _ in range(5):
    bot = Bot(canvas, x=100, y=100)
    env.add_bot(bot)

for _ in range(3):
    obstacle = Obstacle(canvas, x=200, y=200, size=50)
    env.add_obstacle(obstacle)

for _ in range(3):
    plant = Plant(canvas, x=300, y=300)
    env.add_plant(plant)

# Start the simulation
env.run()
```

In this example, we first create a Tkinter window and canvas. We then create an environment and add bots, obstacles, and plants to it. Finally, we start the simulation by calling the `run` method of the `Environment` instance.

## Classes

### Environment

The `Environment` class represents the environment in which the bots, obstacles, and plants exist. It has methods for adding bots, obstacles, and plants to the environment, updating the environment, and running the simulation.

### Bot

The `Bot` class represents a bot. It has an `x` and `y` attribute representing its position in the environment, a `health` attribute, a `move` method for changing its position, and a `take_damage` method for reducing its health.

### Obstacle

The `Obstacle` class represents an obstacle. It has an `x` and `y` attribute representing its position in the environment, and a `size` attribute.

### Plant

The `Plant` class represents a plant. It has an `x` and `y` attribute representing its position in the environment, an `energy` attribute, and a `grow` method for increasing its energy.

Please note that this is a very basic package and you may need to add more functionality to meet your specific needs. For example, you might want to add methods for bots to interact with obstacles and plants, or for plants to be eaten by bots. You might also want to add checks to ensure that bots, obstacles, and plants stay within the bounds of the canvas.
