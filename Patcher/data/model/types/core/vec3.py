import math

from utils.exceptions import ArgumentException


class Vec3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'

    def combine(self, other: 'Vec3') -> 'Vec3':
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def normalize(self) -> 'Vec3':
        magnitude = math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))
        return Vec3(self.x / magnitude, self.y / magnitude, self.z / magnitude)

    def __add__(self, other):
        if isinstance(other, float | int):
            return Vec3(self.x + other, self.y + other, self.z + other)
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        raise NotImplementedError

    def __sub__(self, other):
        if isinstance(other, float | int):
            return Vec3(self.x - other, self.y - other, self.z - other)
        if isinstance(other, Vec3):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        raise NotImplementedError

    def __truediv__(self, other):
        if isinstance(other, float | int):
            return Vec3(self.x / other, self.y / other, self.z / other)
        raise NotImplementedError

    def __mod__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x % other.x, self.y % other.y, self.z % other.z)
        elif isinstance(other, int):
            return Vec3(self.x % other, self.y % other, self.z % other)
        else:
            raise NotImplementedError

    @staticmethod
    def from_yaml(yaml: dict[str, int]) -> 'Vec3':
        x = yaml.get('x', None)
        y = yaml.get('y', None)
        z = yaml.get('z', None)

        if x is None or y is None or z is None:
            raise ArgumentException("Invalid yaml for vec3")

        return Vec3(x=x, y=y, z=z)
