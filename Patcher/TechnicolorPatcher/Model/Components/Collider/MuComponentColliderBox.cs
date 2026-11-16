using TechnicolorPatcher.Types;
using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;

namespace TechnicolorPatcher.Model.Components.Collider;

public class MuComponentColliderBox : IMuComponentCollider
{
    public bool? IsTrigger { get; set; }
    public Vector3 Size { get; set; }
    public Vector3 Center { get; set; }

    public static MuComponentColliderBox Read(MuReader reader, bool hasTrigger)
    {
        bool? isTrigger = hasTrigger ? reader.ReadBoolean() : null;
        Vector3 size = reader.ReadVec3();
        Vector3 center = reader.ReadVec3();

        return new MuComponentColliderBox
        {
            IsTrigger = isTrigger,
            Size = size,
            Center = center
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        if (IsTrigger is null)
        {
            writer.Write(MuTag.ColliderBox);
        }
        else
        {
            writer.Write(MuTag.ColliderBox2);
            writer.Write(IsTrigger.Value);
        }
        
        writer.Write(Size);
        writer.Write(Center);
    }

    public IMuComponent Clone()
    {
        return new MuComponentColliderBox
        {
            IsTrigger = IsTrigger,
            Size = Size,
            Center = Center
        };
    }
}