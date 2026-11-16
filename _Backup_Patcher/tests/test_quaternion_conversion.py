from unittest import TestCase

from data.model.types.core.vec3 import Vec3
from data.model.types.core.vec4 import Vec4
from data.model.types.core.vec_utils import to_quaternion, to_xyz_euler


class TestAngles(TestCase):

    def test_angles(self):
        angles = [
            (Vec4(0.1276795, 0.1448781, 0.2392984, 0.9515485), Vec3(10, 20, 30)),
            (Vec4(0, 0.7071068, 0, -0.7071067),                    Vec3(0, -90, 0)),
            (Vec4(0, 0, 0, 1), Vec3(0, 0, 0)),
        ]

        for angle in angles:
            print()
            print(angle[0])
            xyz = to_xyz_euler(angle[0])
            print(xyz)

            self.assertAlmostEqual(angle[1].x, xyz.x, 4)
            self.assertAlmostEqual(angle[1].y, xyz.y, 4)
            self.assertAlmostEqual(angle[1].z, xyz.z, 4)

            output = to_quaternion(xyz)
            if output.x > 0.000001 > angle[0].x:
                output = Vec4(-output.x, -output.y, -output.z, -output.w)
            elif output.y > 0.000001 > angle[0].y:
                output = Vec4(-output.x, -output.y, -output.z, -output.w)
            elif output.z > 0.000001 > angle[0].z:
                output = Vec4(-output.x, -output.y, -output.z, -output.w)
            elif output.w > 0.000001 > angle[0].w:
                output = Vec4(-output.x, -output.y, -output.z, -output.w)

            print(output)

            dot_expected = angle[0].x**2 + angle[0].y**2 + angle[0].z**2 + angle[0].w**2
            dot_actual = output.x**2 + output.y**2 + output.z**2 + output.w**2

            self.assertAlmostEqual(dot_expected, dot_actual, 4)
