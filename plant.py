class Plant:
    def __init__(self, x, y, energy=100):
        self.x = x
        self.y = y
        self.energy = energy

    def grow(self):
        self.energy += 10
