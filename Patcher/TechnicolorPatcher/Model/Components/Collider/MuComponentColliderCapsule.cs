using TechnicolorPatcher.Types;
using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;

namespace TechnicolorPatcher.Model.Components.Collider;

public class MuComponentColliderCapsule : IMuComponentCollider
{
    public bool? IsTrigger { get; set; }
    public float Radius { get; set; }
    public float Height { get; set; }
    public int Direction { get; set; }
    public Vector3 Center { get; set; }

    public static MuComponentColliderCapsule Read(MuReader reader, bool hasTrigger)
    {
        bool? isTrigger = hasTrigger ? reader.ReadBoolean() : null;
        float radius = reader.ReadSingle();
        float height = reader.ReadSingle();
        int direction = reader.ReadInt32();
        Vector3 center = reader.ReadVec3();

        return new MuComponentColliderCapsule
        {
            IsTrigger = isTrigger,
            Radius = radius,
            Height = height,
            Direction = direction,
            Center = center
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        if (IsTrigger is null)
        {
            writer.Write(MuTag.ColliderCapsule);
        }
        else
        {
            writer.Write(MuTag.ColliderCapsule2);
            writer.Write(IsTrigger.Value);
        }
        
        writer.Write(Radius);
        writer.Write(Height);
        writer.Write(Direction);
        writer.Write(Center);
    }

    public IMuComponent Clone()
    {
        return new MuComponentColliderCapsule
        {
            IsTrigger = IsTrigger,
            Radius = Radius,
            Height = Height,
            Direction = Direction,
            Center = Center
        };
    }
}