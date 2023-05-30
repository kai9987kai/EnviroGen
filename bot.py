class Bot:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print("Bot has been destroyed!")
