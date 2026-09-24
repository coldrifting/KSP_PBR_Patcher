import errno
import os
from pathlib import Path
from typing import Any

from data.model.operation.base import ModelOperation
from data.model.operation.base_factory import ModelOperationFactory
from data.model.types.mu_file import MuFile
from utils.terminal_colors import warn


class ConfigModel:
    def __init__(self, name: str, source: str, operations: list[ModelOperation]):
        self.name = name
        self.source = source
        self.operations = operations

    def __str__(self):
        return "ConfigModel: " + self.name

    def apply(self, game_data_dir: Path, output_dir: Path):
        if len(self.operations) < 1:
            warn(f"{self.source} has no operations defined")
            return

        source_file = Path(game_data_dir / self.source)
        if not source_file.exists():
            source_file = Path(game_data_dir / (self.source + ".mu"))
            if not source_file.exists():
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), source_file)

        mu_data = MuFile.read_file(source_file)
        for operation in self.operations:
            operation.apply(mu_data)

        output_file = Path(output_dir / Path(self.source + ".mu").parts[-1])
        output_file.parent.mkdir(parents=True, exist_ok=True)
        mu_data.write_file(output_file)

    @staticmethod
    def from_yaml(yaml: dict[str, Any], name: str) -> 'ConfigModel':
        return ConfigModel(
            name=name,
            source=yaml['source'],
            operations=[ModelOperationFactory.from_yaml(x) for x in yaml['operations']]
        )
