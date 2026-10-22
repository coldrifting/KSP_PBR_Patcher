from enum import IntEnum

from data.model.types.core.byte_reader import ByteReader
from data.model.types.material.material_property import MaterialProperty, MaterialPropertyTexture, \
    MaterialPropertyColor, MaterialPropertyFloat3


class MaterialTag(IntEnum):
    Custom = 0
    Diffuse = 1
    Specular = 2
    Bumped = 3
    Bumped_Specular = 4
    Emissive = 5
    Emissive_Specular = 6
    Emissive_Bumped_specular = 7
    Alpha_Cutoff = 8
    Alpha_Cutoff_Bumped = 9
    Alpha = 10
    Alpha_Specular = 11
    Alpha_Unlit = 12
    Unlit = 13
    Particles_Alpha_Blended = 14
    Particles_Additive = 15

    @staticmethod
    def read_texture(reader: ByteReader, name: str):
        return MaterialPropertyTexture(name=name,
                                       index=reader.read_int(),
                                       scale=reader.read_vec2(),
                                       offset=reader.read_vec2())

    @staticmethod
    def read_color(reader: ByteReader, name: str):
        return MaterialPropertyColor(name=name,
                                     value=reader.read_vec4())

    @staticmethod
    def read_float(reader: ByteReader, name: str):
        return MaterialPropertyFloat3(name=name,
                                      value=reader.read_float())

    def read_properties(self, reader: ByteReader) -> list[MaterialProperty]:
        match self:
            case MaterialTag.Diffuse:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                return [main_tex]

            case MaterialTag.Specular:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                spec_color = MaterialTag.read_color(reader, name="_SpecColor")
                shininess = MaterialTag.read_float(reader, name="_Shininess")
                return [main_tex, spec_color, shininess]

            case MaterialTag.Bumped:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                bump_map = MaterialTag.read_texture(reader, name="_BumpMap")
                return [main_tex, bump_map]

            case MaterialTag.Bumped_Specular:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                bump_map = MaterialTag.read_texture(reader, name="_BumpMap")
                spec_color = MaterialTag.read_color(reader, name="_SpecColor")
                shininess = MaterialTag.read_float(reader, name="_Shininess")
                return [main_tex, bump_map, spec_color, shininess]

            case MaterialTag.Emissive:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                emissive = MaterialTag.read_texture(reader, name="_Emissive")
                emissive_color = MaterialTag.read_color(reader, name="_EmissiveColor")
                return [main_tex, emissive, emissive_color]

            case MaterialTag.Emissive_Specular:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                spec_color = MaterialTag.read_color(reader, name="_SpecColor")
                shininess = MaterialTag.read_float(reader, name="_Shininess")
                emissive = MaterialTag.read_texture(reader, name="_Emissive")
                emissive_color = MaterialTag.read_color(reader, name="_EmissiveColor")
                return [main_tex, spec_color, shininess, emissive, emissive_color]

            case MaterialTag.Emissive_Bumped_specular:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                bump_map = MaterialTag.read_texture(reader, name="_BumpMap")
                spec_color = MaterialTag.read_color(reader, name="_SpecColor")
                shininess = MaterialTag.read_float(reader, name="_Shininess")
                emissive = MaterialTag.read_texture(reader, name="_Emissive")
                emissive_color = MaterialTag.read_color(reader, name="_EmissiveColor")
                return [main_tex, bump_map, spec_color, shininess, emissive, emissive_color]

            case MaterialTag.Alpha_Cutoff:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                cutoff = MaterialTag.read_float(reader, name="_Cutoff")
                return [main_tex, cutoff]

            case MaterialTag.Alpha_Cutoff_Bumped:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                bump_map = MaterialTag.read_texture(reader, name="_BumpMap")
                cutoff = MaterialTag.read_float(reader, name="_Cutoff")
                return [main_tex, bump_map, cutoff]

            case MaterialTag.Alpha:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                return [main_tex]

            case MaterialTag.Alpha_Specular:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                gloss = MaterialTag.read_float(reader, name="_Gloss")
                spec_color = MaterialTag.read_color(reader, name="_SpecColor")
                shininess = MaterialTag.read_float(reader, name="_Shininess")
                return [main_tex, gloss, spec_color, shininess]

            case MaterialTag.Alpha_Unlit:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                color = MaterialTag.read_color(reader, name="_Color")
                return [main_tex, color]

            case MaterialTag.Unlit:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                color = MaterialTag.read_color(reader, name="_Color")
                return [main_tex, color]

            case MaterialTag.Particles_Alpha_Blended:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                color = MaterialTag.read_color(reader, name="_Color")
                inv_fade = MaterialTag.read_float(reader, name="_InvFade")
                return [main_tex, color, inv_fade]

            case MaterialTag.Particles_Additive:
                main_tex = MaterialTag.read_texture(reader, name="_MainTex")
                color = MaterialTag.read_color(reader, name="_Color")
                inv_fade = MaterialTag.read_float(reader, name="_InvFade")
                return [main_tex, color, inv_fade]

            case _:
                raise NotImplementedError

    def get_shader_name(self):
        match self:
            case MaterialTag.Custom:
                return ""
            case MaterialTag.Diffuse:
                return "KSP/Diffuse"
            case MaterialTag.Specular:
                return "KSP/Specular"
            case MaterialTag.Bumped:
                return "KSP/Bumped"
            case MaterialTag.Bumped_Specular:
                return "KSP/Bumped Specular"
            case MaterialTag.Emissive:
                return "KSP/Emissive"
            case MaterialTag.Emissive_Specular:
                return "KSP/Emissive/Specular"
            case MaterialTag.Emissive_Bumped_specular:
                return "KSP/Emissive/Bumped Specular"
            case MaterialTag.Alpha_Cutoff:
                return "KSP/Alpha/Cutoff"
            case MaterialTag.Alpha_Cutoff_Bumped:
                return "KSP/Alpha/Cutoff Bumped"
            case MaterialTag.Alpha:
                return "KSP/Alpha/Translucent"
            case MaterialTag.Alpha_Specular:
                return "KSP/Alpha/Translucent Specular"
            case MaterialTag.Alpha_Unlit:
                return "KSP/Alpha/Unlit Transparent"
            case MaterialTag.Unlit:
                return "KSP/Unlit"
            case MaterialTag.Particles_Alpha_Blended:
                return "KSP/Particles/Alpha Blended"
            case MaterialTag.Particles_Additive:
                return "KSP/Particles/Additive"

            case _:
                raise NotImplementedError(type(self).__name__)
