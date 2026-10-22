from utils.exceptions import ArgumentException


class Vec4:
    def __init__(self, x: float, y: float, z: float, w: float = 1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z}, {self.w})'

    @staticmethod
    def from_yaml(yaml: dict[str, int]) -> 'Vec4':
        x = yaml.get('x', None)
        y = yaml.get('y', None)
        z = yaml.get('z', None)
        w = yaml.get('w', None)

        if x is None or y is None or z is None or w is None:
            raise ArgumentException("Invalid yaml for vec4")

        return Vec4(x=x, y=y, z=z, w=w)

    def concat(self, other: 'Vec4') -> 'Vec4':
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        return Vec4(x=x, y=y, z=z, w=w)
