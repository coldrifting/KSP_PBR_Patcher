from data.model.types.core.vec4 import Vec4
from data.model.types.mu_file import MuFile
from utils.exceptions import AttributeInvalidError, AttributeNotFoundError


class TeamColor:
    def __init__(self,
                 color: str | Vec4,
                 metalness: float,
                 smoothness: float,
                 metal_blend: float,
                 smooth_blend: float
                 ):
        self.color: Vec4 = color if isinstance(color, Vec4) else TeamColor.get_color(color)
        self.metalness = metalness
        self.smoothness = smoothness
        self.metal_blend = metal_blend
        self.smooth_blend = smooth_blend

    def get_hex_color(self) -> str:
        r = int(self.color.x * 255.0)
        g = int(self.color.y * 255.0)
        b = int(self.color.z * 255.0)
        return f"#{r:02X}{g:02X}{b:02X}".lower()

    @staticmethod
    def apply(mu_data: MuFile, material_name: str, index: int, preset: str):
        tc = TeamColorDb.get(preset, None)
        if tc is None:
            raise AttributeNotFoundError(f'Team Color preset {preset} not found in presets')

        tc.apply_instance(mu_data, material_name, index)

    def apply_instance(self, mu_data: MuFile, material_name: str, index: int):
        mu_data.edit_property(material_name, f"_TC{str(index)}Color", self.color)
        mu_data.edit_property(material_name, f"_TC{str(index)}Metalness", self.metalness)
        mu_data.edit_property(material_name, f"_TC{str(index)}Smoothness", self.smoothness)
        mu_data.edit_property(material_name, f"_TC{str(index)}MetalBlend", self.metal_blend)
        mu_data.edit_property(material_name, f"_TC{str(index)}SmoothBlend", self.smooth_blend)

    @staticmethod
    def get_color(color: str) -> Vec4:
        color_formatted = color
        if color_formatted.startswith("#"):
            color_formatted = color_formatted.lstrip("#")

        if len(color_formatted) != 6 or len(color_formatted) != 8:
            raise AttributeInvalidError(f"Invalid color format: {color}")

        r = float(color_formatted[0:2]) / 255.0
        g = float(color_formatted[2:4]) / 255.0
        b = float(color_formatted[4:6]) / 255.0
        a = float(color_formatted[2:4]) / 255.0 if len(color_formatted) == 8 else 1.0

        return Vec4(r, g, b, a)


# noinspection SpellCheckingInspection
TeamColorDb = {
    # Gloss
    "porkjetWhite":     TeamColor(Vec4(0.85,  0.85,   0.85),  0, 0.75, 1, 1),
    "payloadGrey":      TeamColor(Vec4(0.65,  0.65,   0.65),  0, 0.75, 1, 1),
    "porkjetGrey":      TeamColor(Vec4(0.43,  0.43,   0.43),  0, 0.75, 1, 1),
    "porkjetBlack":     TeamColor(Vec4(0.05,  0.05,   0.05),  0, 0.75, 1, 1),
    "electricalRed":    TeamColor(Vec4(0.678, 0.168,  0.168), 0, 0.75, 1, 1),
    "lithiumRed":       TeamColor(Vec4(0.67,  0.25,   0.20),  0, 0.75, 1, 1),
    "intenseRed":       TeamColor(Vec4(1.0,   0.2,    0.20),  0, 0.75, 1, 1),
    "darkRed":          TeamColor(Vec4(0.34,  0.07,   0.07),  0, 0.75, 1, 1),
    "mediumRed":        TeamColor(Vec4(0.74,  0.18,   0.18),  0, 0.75, 1, 1),
    "rockomaxOrange":   TeamColor(Vec4(0.832, 0.456,  0.201), 0, 0.75, 1, 1),
    "kerbodyneOrange":  TeamColor(Vec4(0.745, 0.39,   0.123), 0, 0.75, 1, 1),
    "atomicOrange":     TeamColor(Vec4(0.881, 0.5588, 0.142), 0, 0.75, 1, 1),
    "drogueOrange":     TeamColor(Vec4(1.0,   0.52,   0.2),   0, 0.75, 1, 1),
    "jebsYellow":       TeamColor(Vec4(0.965, 0.741,  0.08),  0, 0.75, 1, 1),
    "electricalYellow": TeamColor(Vec4(0.852, 0.6707, 0.214), 0, 0.75, 1, 1),
    "intenseYellow":    TeamColor(Vec4(1.0,   0.98,   0.20),  0, 0.75, 1, 1),
    "darkYellow":       TeamColor(Vec4(0.34,  0.35,   0.07),  0, 0.75, 1, 1),
    "mediumYellow":     TeamColor(Vec4(0.847, 0.83,   0.211), 0, 0.75, 1, 1),
    "deltaGreen":       TeamColor(Vec4(0.553, 0.613,  0.373), 0, 0.75, 1, 1),
    "sovietGreen":      TeamColor(Vec4(0.334, 0.367,  0.334), 0, 0.75, 1, 1),
    "methaneGreen":     TeamColor(Vec4(0.372, 0.518,  0.340), 0, 0.75, 1, 1),
    "heliumGreen":      TeamColor(Vec4(0.32,  0.467,  0.454), 0, 0.75, 1, 1),
    "intenseGreen":     TeamColor(Vec4(0.2,   1.0,    0.20),  0, 0.75, 1, 1),
    "darkGreen":        TeamColor(Vec4(0.07,  0.34,   0.07),  0, 0.75, 1, 1),
    "mediumGreen":      TeamColor(Vec4(0.18,  0.74,   0.18),  0, 0.75, 1, 1),
    "intenseCyan":      TeamColor(Vec4(0.2,   0.96,   1.0),   0, 0.75, 1, 1),
    "darkCyan":         TeamColor(Vec4(0.07,  0.34,   0.35),  0, 0.75, 1, 1),
    "mediumCyan":       TeamColor(Vec4(0.21,  0.815,  0.85),  0, 0.75, 1, 1),
    "chuteBlue ":       TeamColor(Vec4(0.32,  0.537,  0.76),  0, 0.75, 1, 1),
    "electricalBlue":   TeamColor(Vec4(0.149, 0.203,  0.6),   0, 0.75, 1, 1),
    "scienceBlue":      TeamColor(Vec4(0.1329,0.629,  0.801), 0, 0.75, 1, 1),
    "deltaBlue":        TeamColor(Vec4(0.278, 0.419,  0.458), 0, 0.75, 1, 1),
    "hydrogenBlue":     TeamColor(Vec4(0.361, 0.521,  0.575), 0, 0.75, 1, 1),
    "deuteriumBlue":    TeamColor(Vec4(0.40,  0.453,  0.566), 0, 0.75, 1, 1),
    "antimatterBlue":   TeamColor(Vec4(0.230, 0.467,  0.650), 0, 0.75, 1, 1),
    "argonBlue":        TeamColor(Vec4(0.321, 0.465,  0.603), 0, 0.75, 1, 1),
    "intenseBlue":      TeamColor(Vec4(0.2,   0.2,    1.0),   0, 0.75, 1, 1),
    "darkBlue":         TeamColor(Vec4(0.07,  0.07,   0.34),  0, 0.75, 1, 1),
    "mediumBlue":       TeamColor(Vec4(0.18,  0.18,   0.74),  0, 0.75, 1, 1),
    "intensePurple":    TeamColor(Vec4(0.57,  0.2,    1.0),   0, 0.75, 1, 1),
    "darkPurple":       TeamColor(Vec4(0.51,  0.07,   0.35),  0, 0.75, 1, 1),
    "mediumPurple":     TeamColor(Vec4(0.2,   0.07,   0.34),  0, 0.75, 1, 1),

    # Matte
    "dullWhite":       TeamColor(Vec4(0.85,  0.85,  0.85), 0, 0.35, 1, 1),
    "melancholyWhite": TeamColor(Vec4(0.65,  0.65,  0.65),  0, 0.35, 1, 1),
    "cloudGrey":       TeamColor(Vec4(0.427, 0.427, 0.427), 0, 0.35, 1, 1),
    "tileBlack":       TeamColor(Vec4(0.05,  0.05,  0.05), 0, 0.35, 1, 1),

    # Metallic
    "metalBasic":    TeamColor(Vec4(0.5,  0.5,    0.5),   1, 0.9, 0, 0),
    "metalBlack":    TeamColor(Vec4(0.1,  0.1,    0.1),   1, 0.9, 0, 0),
    "metalDarkGrey": TeamColor(Vec4(0.35, 0.35,   0.35),  1, 0.9, 0, 0),
    "metalShiny":    TeamColor(Vec4(0.7,  0.7,    0.7),   1, 0.9, 0, 0),
    "metalCopper":   TeamColor(Vec4(0.839, 0.617, 0.439), 1, 0.9, 0, 0),
    "metalGold":     TeamColor(Vec4(0.96,  0.76,  0.356), 1, 0.9, 0, 0),
    "metalBrass":    TeamColor(Vec4(0.858, 0.75,  0.627), 1, 0.9, 0, 0),
    "metalBluish":   TeamColor(Vec4(0.541, 0.583, 0.594), 1, 0.9, 0, 0),

    # MLI
    "mliGold":   TeamColor(Vec4(0.915, 0.751, 0.33), 0.7, 1, 0, 0),
    "mliSilver": TeamColor(Vec4(0.75,  0.75,  0.75), 0.7, 1, 0, 0),
    "mliBlack":  TeamColor(Vec4(0.05,  0.05,  0.05), 0.7, 1, 0, 0),

    # SOFI
    "sofiOrange": TeamColor(Vec4(0.832, 0.456, 0.201), 0, 0.2, 1, 1),
    "sofiYellow": TeamColor(Vec4(0.990, 0.655, 0.228), 0, 0.2, 1, 1),
    "sofiBlue":   TeamColor(Vec4(0.176, 0.423, 0.49),  0, 0.2, 1, 1),
    "sofiBrown":  TeamColor(Vec4(0.575, 0.49,  0.37),  0, 0.2, 1, 1),
    "sofiBeige":  TeamColor(Vec4(0.745, 0.711, 0.657), 0, 0.2, 1, 1),
    "sofiWhite":  TeamColor(Vec4(0.8,   0.8,   0.8),   0, 0.2, 1, 1),

    # Plastic
    "plasticWhite":  TeamColor(Vec4(0.95,  0.95, 0.95),   0, 1, 1, 0.3),
    "plasticBlack":  TeamColor(Vec4(0.05,  0.05, 0.05),   0, 1, 1, 0.3),
    "plasticYellow": TeamColor(Vec4(0.915, 0.715, 0.211), 0, 1, 1, 0.3),
    "plasticRed":    TeamColor(Vec4(0.698, 0.119, 0.101), 0, 1, 1, 0.3),
    "plasticBlue":   TeamColor(Vec4(0.102, 0.153, 0.698), 0, 1, 1, 0.3),

    # Insulation
    "blanketWhite": TeamColor(Vec4(0.85, 0.85,  0.85),  0, 0.3, 1, 1),
    "blanketBeige": TeamColor(Vec4(0.8,  0.786, 0.766), 0, 0.3, 1, 1),
    "blanketBlack": TeamColor(Vec4(0.05, 0.05,  0.05),  0, 0.3, 1, 1),
}