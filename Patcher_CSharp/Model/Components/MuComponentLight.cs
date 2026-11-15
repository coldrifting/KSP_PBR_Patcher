using System.Numerics;
using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model.Components;

public class MuComponentLight : IMuComponent
{
    public int LightType { get; set; }
    public float Intensity { get; set; }
    public float LightRange { get; set; }
    public Vector4 Color { get; set; }
    public int CullingMask { get; set; }
    public float SpotAngle { get; set; }

    public static MuComponentLight Read(MuReader reader)
    {
        int lightType = reader.ReadInt32();
        float intensity = reader.ReadSingle();
        float lightRange = reader.ReadSingle();
        Vector4 color = reader.ReadVec4();
        int cullingMask = reader.ReadInt32();
        float spotAngle = reader.ReadSingle();
        
        return new MuComponentLight
        {
            LightType = lightType,
            Intensity = intensity,
            LightRange = lightRange,
            Color = color,
            CullingMask = cullingMask,
            SpotAngle = spotAngle,
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.Light);
        
        writer.Write(LightType);
        writer.Write(Intensity);
        writer.Write(LightRange);
        writer.Write(Color);
        writer.Write(CullingMask);
        writer.Write(SpotAngle);
    }

    public IMuComponent Clone()
    {
        return new MuComponentLight
        {
            LightType = LightType,
            Intensity = Intensity,
            LightRange = LightRange,
            Color = Color,
            CullingMask = CullingMask,
            SpotAngle = SpotAngle,
        };
    }
}