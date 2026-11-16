using TechnicolorPatcher.Types;
using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;

namespace TechnicolorPatcher.Model.Components.Collider;

public class MuComponentColliderWheel : IMuComponentCollider
{
    public float Mass { get; set; }
    public float Radius { get; set; }
    public float SuspensionDistance { get; set; }
    public Vector3 Center { get; set; }
    public required WheelSpring SuspensionSpring { get; set; }
    public required WheelFriction FrictionForward { get; set; }
    public required WheelFriction FrictionSideways { get; set; }
    
    public static MuComponentColliderWheel Read(MuReader reader)
    {
        float mass = reader.ReadSingle();
        float radius = reader.ReadSingle();
        float suspensionDistance = reader.ReadSingle();
        Vector3 center = reader.ReadVec3();
        
        WheelSpring suspensionSpring = WheelSpring.Read(reader);
        WheelFriction frictionForward = WheelFriction.Read(reader);
        WheelFriction frictionSideways = WheelFriction.Read(reader);
        
        return new MuComponentColliderWheel
        {
            Mass = mass,
            Radius = radius,
            SuspensionDistance = suspensionDistance,
            Center = center,
            SuspensionSpring = suspensionSpring,
            FrictionForward = frictionForward,
            FrictionSideways = frictionSideways
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.ColliderWheel);
        
        writer.Write(Mass);
        writer.Write(Radius);
        writer.Write(SuspensionDistance);
        writer.Write(Center);
        
        SuspensionSpring.Write(writer);
        FrictionForward.Write(writer);
        FrictionSideways.Write(writer);
    }

    public IMuComponent Clone()
    {
        return new MuComponentColliderWheel
        {
            Mass = Mass,
            Radius = Radius,
            SuspensionDistance = SuspensionDistance,
            Center = Center,
            SuspensionSpring = SuspensionSpring.Clone(),
            FrictionForward = FrictionForward.Clone(),
            FrictionSideways = FrictionSideways.Clone()
        };
    }
}