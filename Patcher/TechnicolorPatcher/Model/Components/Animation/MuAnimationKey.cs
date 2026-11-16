using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Types;

namespace TechnicolorPatcher.Model.Components.Animation;

public class MuAnimationKey
{
    public float Time { get; set; }
    public float Value { get; set; }
    public Vector2 TangentInOut { get; set; }
    public int TangentMode { get; set; }

    public static MuAnimationKey Read(MuReader reader)
    {
        float time = reader.ReadSingle();
        float value = reader.ReadSingle();
        Vector2 tangentInOut = reader.ReadVec2();
        int tangentMode = reader.ReadInt32();

        return new MuAnimationKey
        {
            Time = time,
            Value = value,
            TangentInOut = tangentInOut,
            TangentMode = tangentMode
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(Time);
        writer.Write(Value);
        writer.Write(TangentInOut);
        writer.Write(TangentMode);
    }

    public MuAnimationKey Clone()
    {
        return new MuAnimationKey
        {
            Time = Time,
            Value = Value,
            TangentInOut = TangentInOut,
            TangentMode = TangentMode
        };
    }
}