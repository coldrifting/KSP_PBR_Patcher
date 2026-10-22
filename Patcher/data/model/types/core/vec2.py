from utils.exceptions import ArgumentException


class Vec2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    @staticmethod
    def from_yaml(yaml: dict[str, int]) -> 'Vec2':
        x = yaml.get('x', None)
        y = yaml.get('y', None)

        if x is None or y is None:
            raise ArgumentException("Invalid yaml for vec2")

        return Vec2(x=x, y=y)
