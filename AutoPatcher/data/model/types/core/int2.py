class Int2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def clone(self) -> 'Int2':
        return Int2(self.x, self.y)
