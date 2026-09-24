class Vec4:
    def __init__(self, x: float, y: float, z: float, w: float = 1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z}, {self.w})'

    def clone(self) -> 'Vec4':
        return Vec4(self.x, self.y, self.z, self.w)
