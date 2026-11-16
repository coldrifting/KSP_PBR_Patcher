from pathlib import Path

from data.model.mu_data import MuData


class Operation:
    def apply(self, mu_data: MuData, game_data_dir: Path):
        raise NotImplementedError()
