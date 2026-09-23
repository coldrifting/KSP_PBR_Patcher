from pathlib import Path
from unittest import TestCase

from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.mu_file import MuFile


class Test(TestCase):
    def re_encode(self, filename):
        with open(filename, "rb") as f:
            input_bytes = f.read()

        reader = ByteReader(input_bytes)
        mu_file = MuFile.read(reader)

        writer = ByteWriter(ref_data = input_bytes)
        output_bytes = mu_file.write(writer)

        self.assertEqual(input_bytes, output_bytes)

    def test_re_encode_mesh_mk2_cockpit(self):
        self.re_encode(r"/Users/coldrifting/Desktop/Default/restock-pbr-cockpit-mk2-1.mu")

    def test_re_encode_mesh_mk2_cockpit_minimal(self):
        self.re_encode(r"/Users/coldrifting/Desktop/Default/restock-pbr-cockpit-mk2-1-minimal.mu")

    def test_re_encode_mesh_mk2_cockpit_edited(self):
        self.re_encode(r"/Users/coldrifting/Desktop/Default/restock-pbr-cockpit-mk2-1-edited.mu")

    def test_re_encode_mesh_nerv_engine(self):
        self.re_encode(r"/Users/coldrifting/Desktop/Default/restock-pbr-engine-nerv-1.mu")

    def test_re_encode_1(self):
        self.re_encode(r"/Users/coldrifting/Desktop/Default/Disconnected.mu")

    def test_re_encode_2(self):
        self.re_encode(r"/Users/coldrifting/Desktop/Default/DisconnectedWithParent.mu")

    def test_re_encode_3(self):
        self.re_encode(r"/Users/coldrifting/Desktop/Default/Untitled.mu")

    def test_all_restock_pbr_files(self):
        directory = Path("/Users/coldrifting/Desktop/ReStockPBR/GameData")
        for file_path in directory.rglob("*.mu"):
            if file_path.is_file():
                print(file_path)

                # Skip due to bugged extra childTransformEnd tag
                if file_path.name.__contains__("clydesdale"):
                    continue

                self.re_encode(file_path)
