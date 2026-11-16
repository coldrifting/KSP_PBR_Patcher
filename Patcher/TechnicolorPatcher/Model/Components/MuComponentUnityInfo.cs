using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;

namespace TechnicolorPatcher.Model.Components;

public class MuComponentUnityInfo : IMuComponent
{
    public required string Tag { get; set; }
    public int Layer { get; set; }

    public static MuComponentUnityInfo Read(MuReader reader)
    {
        string tag = reader.ReadString();
        int layer = reader.ReadInt32();

        return new MuComponentUnityInfo
        {
            Tag = tag,
            Layer = layer
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.UnityInfo);
        
        writer.Write(Tag);
        writer.Write(Layer);
    }

    public IMuComponent Clone()
    {
        return new MuComponentUnityInfo()
        {
            Tag = Tag,
            Layer = Layer
        };
    }
}