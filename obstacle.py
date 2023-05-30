from tkinter import Canvas

class Obstacle:
    def __init__(self, canvas: Canvas, x: int, y: int, size: int):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.shape = canvas.create_rectangle(x, y, x + size, y + size, fill='blue')
