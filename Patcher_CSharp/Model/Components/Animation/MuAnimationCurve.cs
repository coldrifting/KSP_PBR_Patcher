using KSP_PBR_Patcher.Model.IO;

namespace KSP_PBR_Patcher.Model.Components.Animation;

public class MuAnimationCurve
{
    public required string Name { get; set; }
    public required string Property { get; set; }
    public int Type { get; set; }
    public int WrapModeIn { get; set; }
    public int WrapModeOut { get; set; }
    public required MuAnimationKey[] Keys { get; set; }

    public static MuAnimationCurve Read(MuReader reader)
    {
        string name = reader.ReadString();
        string property = reader.ReadString();
        int type = reader.ReadInt32();
        int wrapModeIn = reader.ReadInt32();
        int wrapModeOut = reader.ReadInt32();

        int numKeys = reader.ReadInt32();
        MuAnimationKey[] keys = new MuAnimationKey[numKeys];
        for (int i = 0; i < numKeys; i++)
        {
            keys[i] = MuAnimationKey.Read(reader);
        }

        return new MuAnimationCurve
        {
            Name = name,
            Property = property,
            Type = type,
            WrapModeIn = wrapModeIn,
            WrapModeOut = wrapModeOut,
            Keys = keys
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(Name);
        writer.Write(Property);
        writer.Write(Type);
        writer.Write(WrapModeIn);
        writer.Write(WrapModeOut);
        
        writer.Write(Keys.Length);
        foreach (MuAnimationKey key in Keys)
        {
            key.Write(writer);
        }
    }

    public MuAnimationCurve Clone()
    {
        return new MuAnimationCurve
        {
            Name = Name,
            Property = Property,
            Type = Type,
            WrapModeIn = WrapModeIn,
            WrapModeOut = WrapModeOut,
            Keys = Keys.Select(k => k.Clone()).ToArray()
        };
    }
}