from pathlib import Path
from typing import Any, Tuple, cast

import numpy as np
from PIL import Image
from scipy.interpolate import CubicSpline

from data.texture.layer.base import Layer
from utils.exceptions import ArgumentException


class Curves(Layer):
    def __init__(self, points: list[Tuple[int, int]], masks: list[Tuple[str, bool]], invert_masks: bool, group_type: str):
        super().__init__(masks, invert_masks, group_type)

        self.points = points

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              config_path: Path,
              game_data: Path):
        lut = generate_lut(self.points) * 3
        layer_image = image.point(lut)

        self.apply_mask(
            image=image,
            layer_image=layer_image,
            config_path=config_path
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any], masks: list[tuple[str, bool]], group_type: str) -> 'Curves':
        points_yaml: list[list[int]] | None = yaml.get("points", None)
        if points_yaml is None:
            raise ArgumentException("Missing required parameter 'points' for effect curves")

        if not is_list_of_list_of_nums(points_yaml):
            raise ArgumentException("Invalid points parameter for effect curves:\r\n"
                                    f"{points_yaml}")

        points: list[Tuple[int, int]] = []
        for point in points_yaml:
            points.append((int(point[0]), int(point[1])))

        if points[-1][0] != 255:
            points.append((255, 255))

        if points[0][0] != 0:
            points.insert(0, (0, 0))

        return Curves(
            points=points,
            masks=masks,
            invert_masks=yaml.get("invert_masks", False),
            group_type=group_type
        )


def generate_lut(points: list[Tuple[int, int]]) -> list[int]:
    x_pts = [p[0] for p in points]
    y_pts = [p[1] for p in points]

    # Ensure boundary conditions clamp properly to 0-255
    cs = CubicSpline(x_pts, y_pts, bc_type='natural')

    x_vals = np.arange(256)
    y_vals = cs(x_vals)

    # Clip values to valid 0-255 image byte range
    return cast(list[int],np.clip(y_vals, 0, 255).astype(np.uint8).tolist())


def is_list_of_list_of_nums(data):
    return (
            isinstance(data, list) and
            all(len(sub) == 2 for sub in data) and
            all(isinstance(sub, list) for sub in data) and
            all(type(item) is float or type(item) is int for sub in data for item in sub)
    )
