using KSP_PBR_Patcher.Model.IO;

namespace KSP_PBR_Patcher.Model.Components.Collider;

public class WheelSpring
{
    public float Spring { get; set; }
    public float Damper { get; set; }
    public float TargetPos { get; set; }

    public static WheelSpring Read(MuReader reader)
    {
        float spring = reader.ReadSingle();
        float damper = reader.ReadSingle();
        float targetPos = reader.ReadSingle();

        return new WheelSpring
        {
            Spring = spring,
            Damper = damper,
            TargetPos = targetPos
        };
    }

    public void Write(BinaryWriter writer)
    {
        writer.Write(Spring);
        writer.Write(Damper);
        writer.Write(TargetPos);
    }

    public WheelSpring Clone()
    {
        return new WheelSpring
        {
            Spring = Spring,
            Damper = Damper,
            TargetPos = TargetPos
        };
    }
}