class Vec2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def clone(self) -> 'Vec2':
        return Vec2(self.x, self.y)
