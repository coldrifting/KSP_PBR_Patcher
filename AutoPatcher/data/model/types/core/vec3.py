import math


class Vec3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'

    def clone(self) -> 'Vec3':
        return Vec3(self.x, self.y, self.z)

    def combine(self, other: 'Vec3') -> 'Vec3':
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def normalize(self) -> 'Vec3':
        magnitude = math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))
        return Vec3(self.x / magnitude, self.y / magnitude, self.z / magnitude)

    def __add__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, float | int):
            return Vec3(self.x / other, self.y / other, self.z / other)
        return NotImplemented