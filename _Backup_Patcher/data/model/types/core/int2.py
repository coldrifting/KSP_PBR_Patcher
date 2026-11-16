from utils.exceptions import ArgumentException


class Int2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def clone(self) -> 'Int2':
        return Int2(self.x, self.y)

    @staticmethod
    def from_yaml(yaml: dict[str, int]) -> 'Int2':
        x = yaml.get('x', None)
        y = yaml.get('y', None)

        if x is None or y is None:
            raise ArgumentException("Invalid yaml for int2")

        return Int2(x=x, y=y)
