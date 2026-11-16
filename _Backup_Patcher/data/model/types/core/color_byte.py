class ColorByte:
    def __init__(self, r: int, g: int, b: int, a: int):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __str__(self) -> str:
        return f'rgba({self.r}, {self.g}, {self.b}, {self.a})'

    def clone(self) -> 'ColorByte':
        return ColorByte(self.r, self.g, self.b, self.a)
