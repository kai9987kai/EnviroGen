class Bot:
    def __init__(self, canvas: tk.Canvas, x: int, y: int, health: int = 100):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.health = health
        self.shape = canvas.create_rectangle(x, y, x + 10, y + 10, fill='red')

    def move(self, dx: int = 1, dy: int = 1):
        self.x += dx
        self.y += dy
        self.canvas.move(self.shape, dx, dy)

    def take_damage(self, amount: int):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.canvas.delete(self.shape)
