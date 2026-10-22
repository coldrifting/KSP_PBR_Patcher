import math

from data.model.types.core.vec3 import Vec3
from data.model.types.core.vec4 import Vec4

def to_xyz_euler(q: Vec4) -> Vec3:
    unit = (q.x * q.x) + (q.y * q.y) + (q.z * q.z) + (q.w * q.w)
    test = q.x * q.w - q.y * q.z

    # North pole singularity
    if test > 0.4995 * unit:
        x = math.pi / 2
        y = 2 * math.atan2(q.y, q.x)
        z = 0
    # South pole singularity
    elif test < -0.4995 * unit:
        x = -math.pi / 2
        y = -2 * math.atan2(q.y, q.x)
        z = 0
    else:
        x = math.asin(2 * (q.w * q.x - q.y * q.z))
        y = math.atan2(2 * q.w * q.y + 2 * q.z * q.x, 1 - 2 * (q.x * q.x + q.y * q.y))
        z = math.atan2(2 * q.w * q.z + 2 * q.x * q.y, 1 - 2 * (q.z * q.z + q.x * q.x))

    x = math.degrees(x)
    y = math.degrees(y)
    z = math.degrees(z)

    # Normalize to range of -360, 360
    x = ((x + 360) % 720) - 360
    y = ((y + 360) % 720) - 360
    z = ((z + 360) % 720) - 360

    return Vec3(x, y, z)

def to_quaternion(vector: Vec3) -> Vec4:
    x_over_2 = math.radians(vector.x) * 0.5
    y_over_2 = math.radians(vector.y) * 0.5
    z_over_2 = math.radians(vector.z) * 0.5

    sinx_over_2 = math.sin(x_over_2)
    cosx_over_2 = math.cos(x_over_2)
    siny_over_2 = math.sin(y_over_2)
    cosy_over_2 = math.cos(y_over_2)
    sinz_over_2 = math.sin(z_over_2)
    cosz_over_2 = math.cos(z_over_2)

    x = cosy_over_2 * sinx_over_2 * cosz_over_2 + siny_over_2 * cosx_over_2 * sinz_over_2
    y = siny_over_2 * cosx_over_2 * cosz_over_2 - cosy_over_2 * sinx_over_2 * sinz_over_2
    z = cosy_over_2 * cosx_over_2 * sinz_over_2 - siny_over_2 * sinx_over_2 * cosz_over_2
    w = cosy_over_2 * cosx_over_2 * cosz_over_2 + siny_over_2 * sinx_over_2 * sinz_over_2

    return Vec4(x, y, z, w)
