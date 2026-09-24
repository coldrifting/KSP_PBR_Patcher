from pathlib import Path
from typing import Any, Tuple

import numpy as np
from PIL import Image

from data.texture.layer.base import Layer
from utils.exceptions import ArgumentException


class Noise(Layer):
    def __init__(self, intensity: float | int, coverage: float | int, masks: list[Tuple[str, bool]], invert_masks: bool, group_type: str):
        super().__init__(masks, invert_masks, group_type)

        self.intensity = intensity
        self.coverage = coverage

    def apply(self,
              size: Tuple[int, int],
              prev_channels: dict[str, Image.Image],
              image: Image.Image,
              config_path: Path,
              game_data: Path):

        layer_image = add_noise(image, self.intensity, self.coverage)

        self.apply_mask(
            image=image,
            layer_image=layer_image,
            config_path=config_path
        )

    @staticmethod
    def from_yaml(yaml: dict[str, Any], masks: list[tuple[str, bool]], group_type: str) -> 'Noise':
        intensity: float | int | None = yaml.get("intensity", None)
        if intensity is None:
            raise ArgumentException("Missing required parameter 'radius' for effect blur")

        if intensity > 100 or intensity < 0:
            raise ArgumentException(f"Invalid intensity parameter {intensity}. Must be between 0 and 100")

        coverage: float | int | None = yaml.get("coverage", None)
        if coverage is None:
            coverage = 50

        if coverage > 100 or coverage < 0:
            raise ArgumentException(f"Invalid coverage parameter {coverage}. Must be between 0 and 100")

        return Noise(
            intensity=intensity,
            coverage=coverage,
            masks=masks,
            invert_masks=yaml.get("invert_masks", False),
            group_type=group_type
        )


def add_noise(image: Image.Image, intensity: int, coverage: int = 100) -> Image.Image:
    image_array = np.array(image.convert("RGB"), dtype=np.uint8)

    # Remap intensity to be exponential
    intensity = (intensity * intensity) / 100

    rng = np.random.default_rng()
    noise_1d = (rng.uniform(low=-1.0, high=1.0, size=image.size) * ((intensity / 100.0) * 127.0)).astype(int)
    noise_3d = np.dstack([noise_1d] * 3)

    noise_applied = np.clip(image_array + noise_3d, 0, 255).astype(np.uint8)

    image_with_noise = Image.fromarray(noise_applied)

    # Coverage: Percentage of pixels (chosen at random) that have noise applied
    coverage_array = np.ones(image.size).astype(np.uint8) * 255
    if coverage != 100:
        num_zeros = int(((100 - coverage) / 100.0) * image.size[0] * image.size[1])
        for i in range(num_zeros):
            coverage_array.flat[i] = 0

        coverage_array_flat = coverage_array.ravel()
        rng.shuffle(coverage_array_flat)
        coverage_array = coverage_array_flat.reshape(image.size)

    coverage_mask_image = Image.fromarray(coverage_array)

    output = image.copy()
    output.paste(image_with_noise, None, coverage_mask_image)

    return output

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)