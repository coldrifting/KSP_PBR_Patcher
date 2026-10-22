from pathlib import Path
from unittest import TestCase

from data.model.types.core.byte_writer import ByteWriter
from data.model.mu_data import MuData
from utils.printing import warn


class TestReadAndWrite(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gamedata_dir = Path(r"C:\Steam\steamapps\common\Kerbal Space Program\GameData")

    def test_v0_file(self):
        self.test_file(r"")

    def test_v1_file(self):
        self.test_file(r"Squad\Parts\Aero\wingletDeltaDeluxe\model.mu")

    def test_v2_file(self):
        self.test_file(r"Squad\Parts\Aero\wingletAV-R8\model.mu")

    def test_v3_file(self):
        self.test_file(r"Squad\Parts\Aero\airbrake\Airbrake.mu")

    def test_v4_file(self):
        self.test_file(r"Squad\Parts\Aero\fairings\AutoTruss.mu")

    def test_v5_file(self):
        self.test_file(r"Squad\Parts\Aero\aerodynamicNoseCone\aerodynamicNoseCone.mu")

    def test_single_file(self):
        self.test_file(r"Squad\Parts\Resources\MiniDrill\MiniDrill.mu")

    def test_all_files(self):
        directories = [
            "Squad/Parts",
            "SquadExpansion/Serenity/Parts"
            "SquadExpansion/MakingHistory/Parts",
            "ReStock/Assets",
            "ReStockPlus/Assets",
            "ReStockPBR",
            "ReStockPlusPBR"
        ]

        model_files: list[Path] = []
        for directory in directories:
            mod_dir = self.gamedata_dir / directory
            mod_model_files: list[Path] = list(mod_dir.glob("**/*.mu"))
            model_files.extend(mod_model_files)

        for model_file in model_files:
            if "clydesdale" in model_file.name:
                continue # Ignore bugged mesh_components file

            TestReadAndWrite.read_and_write(self, model_file)


    def test_file(self, path):
        full_path = self.gamedata_dir / Path(path)
        self.read_and_write(full_path)

    def read_and_write(self, model_path: Path):
            write_output: bool = True

            input_data = model_path.read_bytes()

            sub_path = model_path.relative_to(TestReadAndWrite.gamedata_dir)
            print(sub_path)

            version = int.from_bytes(input_data[4:8], byteorder="little")

            try:
                if not version == 5:
                    warn(f"Mu file version {version} is not the latest (5). Skipping detailed equality checks...")

                    # Can't compare very well, so check rewrite doesn't change things
                    mu_file_old = MuData.from_bytes(input_data)
                    input_data = mu_file_old.write_bytes()

                    if write_output:
                        output_file = Path(r"C:\Users\coldrifting\Desktop\converted.mu")
                        output_file.write_bytes(input_data)


                mu_file = MuData.from_bytes(input_data)
                output_data = mu_file.write_bytes(ByteWriter(input_data))

            except Exception:
                print(f"{sub_path} failed to read and write")
                raise

            self.assertEqual(len(output_data), len(input_data), msg=f"{sub_path} output length did not match input length")

            if write_output:
                output_dir = Path(r"C:\Users\coldrifting\Desktop\Output")
                output_dir.mkdir(parents=True, exist_ok=True)

                output_file = (output_dir / Path(model_path.name)).with_suffix(".mu")

                output_file.write_bytes(output_data)
