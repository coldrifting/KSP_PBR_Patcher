using TechnicolorPatcher.Types;
using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;

namespace TechnicolorPatcher.Model.Components.Collider;

public class MuComponentColliderSphere : IMuComponentCollider
{
    public bool? IsTrigger { get; set; }
    public float Radius { get; set; }
    public Vector3 Center { get; set; }

    public static MuComponentColliderSphere Read(MuReader reader, bool hasTrigger)
    {
        bool? isTrigger = hasTrigger ? reader.ReadBoolean() : null;
        float radius = reader.ReadSingle();
        Vector3 center = reader.ReadVec3();

        return new MuComponentColliderSphere
        {
            IsTrigger = isTrigger,
            Radius = radius,
            Center = center
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        if (IsTrigger is null)
        {
            writer.Write(MuTag.ColliderSphere);
        }
        else
        {
            writer.Write(MuTag.ColliderSphere2);
            writer.Write(IsTrigger.Value);
        }
        
        writer.Write(Radius);
        writer.Write(Center);
    }

    public IMuComponent Clone()
    {
        return new MuComponentColliderSphere
        {
            IsTrigger = IsTrigger,
            Radius = Radius,
            Center = Center
        };
    }
}