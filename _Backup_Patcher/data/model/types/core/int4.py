class Int4:
    def __init__(self, x: int, y: int, z: int, w: int):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z}, {self.w})'

    def clone(self) -> 'Int4':
        return Int4(self.x, self.y, self.z, self.w)
