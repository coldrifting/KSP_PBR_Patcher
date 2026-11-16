using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Types;

[YamlSerializable]
public struct Vector3(float x, float y, float z)
{
    public float X { get; set; } = x;
    public float Y { get; set; } = y;
    public float Z { get; set; } = z;

    public static Vector3 Zero => new(0, 0, 0);
    public static Vector3 One => new(1, 1, 1);

    public static Vector3 operator +(Vector3 a, Vector3 b)
    {
        return new Vector3(a.X + b.X, a.Y + b.Y, a.Z + b.Z);
    } 

    public static Vector3 operator /(Vector3 a, float b)
    {
        return new Vector3(a.X / b, a.Y / b, a.Z / b);
    }
    
    public static Vector3 Normalize(Vector3 v)
    {
        float divisor = (float)Math.Sqrt(v.X * v.X + v.Y * v.Y + v.Z * v.Z);
        return v / divisor;
    }
}