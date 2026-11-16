using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;

namespace TechnicolorPatcher.Model.Components;

public class MuComponentRenderer : IMuComponent
{
    public bool ShadowCast { get; set; }
    public bool ShadowReceive { get; set; }
    public int MaterialCount { get; set; }
    public int MaterialIndex { get; set; }

    public static MuComponentRenderer Read(MuReader reader)
    {
        bool shadowCast = reader.Version < 1 || reader.ReadBoolean();
        bool shadowReceive = reader.Version < 1 || reader.ReadBoolean();

        int materialCount = reader.ReadInt32();
        int materialIndex = reader.ReadInt32();

        return new MuComponentRenderer
        {
            ShadowCast = shadowCast,
            ShadowReceive = shadowReceive,
            MaterialCount = materialCount,
            MaterialIndex = materialIndex
        };
    }

    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.MeshRenderer);

        writer.Write(ShadowCast);
        writer.Write(ShadowReceive);
        writer.Write(MaterialCount);
        writer.Write(MaterialIndex);
    }

    public IMuComponent Clone()
    {
        return new MuComponentRenderer
        {
            ShadowCast = ShadowCast,
            ShadowReceive = ShadowReceive,
            MaterialCount = MaterialCount,
            MaterialIndex = MaterialIndex
        };
    }
}