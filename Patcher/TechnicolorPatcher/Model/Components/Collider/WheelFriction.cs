using TechnicolorPatcher.Model.IO;

namespace TechnicolorPatcher.Model.Components.Collider;

public class WheelFriction
{
    public float ExtremumSlip { get; set; }
    public float ExtremumValue { get; set; }
    public float AsymptoteSlip { get; set; }
    public float AsymptoteValue { get; set; }
    public float Stiffness { get; set; }

    public static WheelFriction Read(MuReader reader)
    {
        float extremumSlip = reader.ReadSingle();
        float extremumValue = reader.ReadSingle();
        float asymptoteSlip = reader.ReadSingle();
        float asymptoteValue = reader.ReadSingle();
        float stiffness = reader.ReadSingle();

        return new WheelFriction
        {
            ExtremumSlip = extremumSlip,
            ExtremumValue = extremumValue,
            AsymptoteSlip = asymptoteSlip,
            AsymptoteValue = asymptoteValue,
            Stiffness = stiffness
        };
    }

    public void Write(BinaryWriter writer)
    {
        writer.Write(ExtremumSlip);
        writer.Write(ExtremumValue);
        writer.Write(AsymptoteSlip);
        writer.Write(AsymptoteValue);
        writer.Write(Stiffness);
    }

    public WheelFriction Clone()
    {
        return new WheelFriction
        {
            ExtremumSlip = ExtremumSlip,
            ExtremumValue = ExtremumValue,
            AsymptoteSlip = AsymptoteSlip,
            AsymptoteValue = AsymptoteValue,
            Stiffness = Stiffness
        };
    }
}