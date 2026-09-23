from typing import Any, Tuple

from utils.exceptions import ArgumentException, AttributeInvalidError
from utils.string_writer import StringWriter
from utils.team_color import TeamColor, TeamColorDb


class ConfigPartMaterialDef:
    def __init__(self,
                 name: str,
                 main_tex: str,
                 bump_map: str | None,
                 emissive: str | None,
                 metal_map: str,
                 team_color_map: str | None,
                 tc1: Tuple[str, TeamColor] | None,
                 tc2: Tuple[str, TeamColor] | None):
        self.name = name
        self.main_tex = main_tex
        self.bump_map = bump_map
        self.emissive = emissive
        self.metal_map = metal_map
        self.team_color_map = team_color_map
        self.tc1 = tc1
        self.tc2 = tc1 if tc2 is None else tc2

    def write(self) -> str:
        writer : StringWriter = StringWriter()

        writer.write("SHABBY_MATERIAL_DEF")

        writer.indent()
        writer.write(f"name = {self.name}")

        if self.tc1 is not None:
            writer.write(f"shader = Resurfaced/Standard (TC)")
        else:
            writer.write(f"shader = Resurfaced/Standard")

        writer.write()

        writer.write("TEXTURE")
        writer.indent()

        writer.write(f"_MainTex = {self.main_tex}")
        if self.bump_map is not None:
            writer.write(f"_BumpMap = {self.bump_map}")
        if self.emissive is not None:
            writer.write(f"_Emissive = {self.emissive}")
        writer.write(f"_MetalMap = {self.metal_map}")
        if self.team_color_map is not None:
            writer.write(f"_TeamColorMap = {self.team_color_map}")

        writer.unindent()

        writer.write()

        if self.tc1 is not None:
            writer.write(f"// {self.tc1[0]}, {self.tc2[0]}")
            writer.write("COLOR")
            writer.indent()
            writer.write(f"_TC1Color = {self.tc1[1].get_hex_color()}")
            writer.write(f"_TC2Color = {self.tc2[1].get_hex_color()}")
            writer.unindent()

            writer.write("FLOAT")
            writer.indent()
            writer.write(f"_TC1Metalness = {self.tc1[1].metalness}")
            writer.write(f"_TC1Smoothness = {self.tc1[1].smoothness}")
            writer.write(f"_TC1MetalBlend = {self.tc1[1].metal_blend}")
            writer.write(f"_TC1SmoothBlend = {self.tc1[1].smooth_blend}")
            writer.write()
            writer.write(f"_TC2Metalness = {self.tc2[1].metalness}")
            writer.write(f"_TC2Smoothness = {self.tc2[1].smoothness}")
            writer.write(f"_TC2MetalBlend = {self.tc2[1].metal_blend}")
            writer.write(f"_TC2SmoothBlend = {self.tc2[1].smooth_blend}")
            writer.unindent()

        writer.unindent()

        return writer.get_string()

    @staticmethod
    def from_yaml(yaml: dict[str, Any]) -> 'ConfigPartMaterialDef':
        name: str | None = yaml.get("name", None)
        if name is None:
            raise ArgumentException("Missing name value for material")

        main_tex: str | None = yaml.get("main_tex", None)
        if main_tex is None:
            raise ArgumentException("Missing main_tex value for material")

        bump_map: str | None = yaml.get("bump_map", None)
        emissive: str | None = yaml.get("emissive", None)
        metal_map: str | None = yaml.get("metal_map", None)
        team_color_map: str | None = yaml.get("team_color_map", None)

        tc1 = None
        tc1_name: str | None = yaml.get("tc1", None)
        if tc1_name is not None:
            tc1_color = TeamColorDb.get(tc1_name, None)
            if tc1_color is None:
                raise AttributeInvalidError(f"Team Color 1 preset {tc1_name} not found for material")

            tc1 = (tc1_name, tc1_color)

        tc2 = None
        tc2_name: str | None = yaml.get("tc2", None)
        if tc2_name is None or tc2_name.lower() == "blank":
            tc2 = tc1
        else:
            if tc2_name is not None:
                tc2_color = TeamColorDb.get(tc2_name, None)
                if tc2_color is None:
                    raise AttributeInvalidError(f"Team Color 2 preset {tc2_name} not found for material")

                tc2 = (tc2_name, tc2_color)

        return ConfigPartMaterialDef(
            name=name,
            main_tex=main_tex,
            bump_map=bump_map,
            emissive=emissive,
            metal_map=metal_map,
            team_color_map=team_color_map,
            tc1=tc1,
            tc2=tc2
        )
