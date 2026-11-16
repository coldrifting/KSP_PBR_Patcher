using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;

namespace TechnicolorPatcher.Model.Components.Collider;

public class MuComponentColliderMesh : IMuComponentCollider
{
    public bool? IsTrigger { get; set; }
    public bool IsConvex { get; set; }
    public required MuComponentMesh Mesh { get; set; }

    public static MuComponentColliderMesh Read(MuReader reader, bool hasTrigger)
    {
        bool? isTrigger = hasTrigger ? reader.ReadBoolean() : null;
        bool isConvex = reader.ReadBoolean();
        MuComponentMesh mesh = MuComponentMesh.Read(reader);
        mesh.HasFilter = false;
        
        return new MuComponentColliderMesh
        {
            IsTrigger = isTrigger,
            IsConvex = isConvex,
            Mesh = mesh
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        if (IsTrigger is null)
        {
            writer.Write(MuTag.ColliderMesh);
        }
        else
        {
            writer.Write(MuTag.ColliderMesh2);
            writer.Write(IsTrigger.Value);
        }
        
        writer.Write(IsConvex);
        Mesh.Write(writer);
    }

    public IMuComponent Clone()
    {
        return new MuComponentColliderMesh
        {
            IsTrigger = IsTrigger,
            IsConvex = IsConvex,
            Mesh = (MuComponentMesh)Mesh.Clone()
        };
    }
}