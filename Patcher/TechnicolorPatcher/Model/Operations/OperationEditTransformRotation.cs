using TechnicolorPatcher.Types;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Model.Operations;

[YamlSerializable]
public class OperationEditTransformRotation : OperationBase
{
    public static string OperationName => "edit_transform_rotation";

    public required string Transform { get; set; }
    public Vector3 Rotation { get; set; }
    public bool Absolute { get; set; }

    public override void Apply(MuFile muFile, string gameDataPath)
    {
        List<MuTransform> transforms = muFile.GetTransforms(Transform);
        if (transforms.Count == 0)
        {
            throw new ArgumentException($"No transforms found with name {Transform}");
        }

        foreach (MuTransform transform in transforms)
        {
            Vector3 transformRotation = Absolute ? new Vector3(0, 0, 0) : ToXyzEuler(transform.Rotation);
            Vector3 newRotation = transformRotation + Rotation;
            float x = ((newRotation.X + 360) % 720) - 360;
            float y = ((newRotation.Y + 360) % 720) - 360;
            float z = ((newRotation.Z + 360) % 720) - 360;
            Vector3 normalizedRotation = new(x, y, z);
            Vector4 rotationQuaternion = ToQuaternion(normalizedRotation);
            transform.Rotation = rotationQuaternion;
        }
    }

    private static Vector3 ToXyzEuler(Vector4 q)
    {
        float unit = (q.X * q.X) + (q.Y * q.Y) + (q.Z * q.Z) + (q.W * q.W);
        float test = q.X * q.W - q.Y * q.Z;

        float x;
        float y;
        float z;
        
        // North-pole singularity
        if (test > 0.4995 * unit)
        {
            x = (float)(Math.PI / 2);
            y = (float)(2 * Math.Atan2(q.Y, q.X));
            z = 0;
        }

        // South-pole singularity
        else if (test < -0.4995 * unit)
        {
            x = (float)(-Math.PI / 2);
            y = (float)(-2 * Math.Atan2(q.Y, q.X));
            z = 0;
        }
        else
        {
            x = (float)Math.Asin(2 * (q.W * q.X - q.Y * q.Z));
            y = (float)Math.Atan2(2 * q.W * q.Y + 2 * q.Z * q.X, 1 - 2 * (q.X * q.X + q.Y * q.Y));
            z = (float)Math.Atan2(2 * q.W * q.Z + 2 * q.X * q.Y, 1 - 2 * (q.Z * q.Z + q.X * q.X));
        }

        x = float.RadiansToDegrees(x);
        y = float.RadiansToDegrees(y);
        z = float.RadiansToDegrees(z);

        // Normalize to range of -360, 360
        x = ((x + 360) % 720) - 360;
        y = ((y + 360) % 720) - 360;
        z = ((z + 360) % 720) - 360;

        return new Vector3(x, y, z);
    }

    private static Vector4 ToQuaternion(Vector3 vector)
    {
        double xOver2 = float.DegreesToRadians(vector.X) * 0.5;
        double yOver2 = float.DegreesToRadians(vector.Y) * 0.5;
        double zOver2 = float.DegreesToRadians(vector.Z) * 0.5;

        double sinxOver2 = Math.Sin(xOver2);
        double cosxOver2 = Math.Cos(xOver2);
        double sinyOver2 = Math.Sin(yOver2);
        double cosyOver2 = Math.Cos(yOver2);
        double sinzOver2 = Math.Sin(zOver2);
        double coszOver2 = Math.Cos(zOver2);

        float x = (float)(cosyOver2 * sinxOver2 * coszOver2 + sinyOver2 * cosxOver2 * sinzOver2);
        float y = (float)(sinyOver2 * cosxOver2 * coszOver2 - cosyOver2 * sinxOver2 * sinzOver2);
        float z = (float)(cosyOver2 * cosxOver2 * sinzOver2 - sinyOver2 * sinxOver2 * coszOver2);
        float w = (float)(cosyOver2 * cosxOver2 * coszOver2 + sinyOver2 * sinxOver2 * sinzOver2);

        return new Vector4(x, y, z, w);
    }
}
