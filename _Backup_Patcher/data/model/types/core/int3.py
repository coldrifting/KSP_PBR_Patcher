class Int3:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'

    def clone(self) -> 'Int3':
        return Int3(self.x, self.y, self.z)
