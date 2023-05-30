from tkinter import Canvas

class Plant:
    def __init__(self, canvas: Canvas, x: int, y: int, energy: int = 100):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.energy = energy
        self.shape = canvas.create_oval(x, y, x + 10, y + 10, fill='green')

    def grow(self):
        self.energy += 10
