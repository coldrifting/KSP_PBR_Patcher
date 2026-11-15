using System.Numerics;
using KSP_PBR_Patcher.Model.Tags;
using KSP_PBR_Patcher.Types;

namespace KSP_PBR_Patcher.Model.IO;

public class MuReader
{
    public BinaryReader Reader { get; }
    public int Version { get; }

    public const int MagicNumber = 76543;

    public MuReader(string path)
    {
        Reader = new BinaryReader(File.OpenRead(path));
        int fileMagic = Reader.ReadInt32();
        if (fileMagic != MagicNumber)
        {
            throw new InvalidDataException($"Not a valid Mu model file: \n{path}");
        }
        
        Version = Reader.ReadInt32();
    }

    public void Rewind(int count)
    {
        Reader.BaseStream.Position -= count;
    }

    public MuTag ReadTag()
    {
        int rawTag = Reader.ReadInt32();
        MuTag tag = (MuTag)rawTag;
        if (Enum.IsDefined(tag))
        {
            return tag;
        }

        throw new InvalidDataException($"Invalid tag - {rawTag}");
    }

    public bool ReadBoolean()
    {
        return Reader.ReadBoolean();
    }
    
    public int ReadInt32()
    {
        return Reader.ReadInt32();
    }
    
    public uint ReadUInt32()
    {
        return Reader.ReadUInt32();
    }

    public float ReadSingle()
    {
        return Reader.ReadSingle();
    }

    public string ReadString()
    {
        // TODO - does this need to be changed for variable length strings?
        return Reader.ReadString();
    }

    public BoneWeight ReadBoneWeight()
    {
        Int4 indices = ReadInt4();
        Vector4 weights = ReadVec4();
        return new BoneWeight(indices, weights);
    }

    public Int3 ReadInt3()
    {
        int x = Reader.ReadInt32();
        int y = Reader.ReadInt32();
        int z = Reader.ReadInt32();
        return new Int3(x, y, z);
    }

    public Int4 ReadInt4()
    {
        int x = Reader.ReadInt32();
        int y = Reader.ReadInt32();
        int z = Reader.ReadInt32();
        int w = Reader.ReadInt32();
        return new Int4(x, y, z, w);
    }

    public ColorByte ReadColorByte()
    {
        byte r = Reader.ReadByte();
        byte g = Reader.ReadByte();
        byte b = Reader.ReadByte();
        byte a = Reader.ReadByte();
        return new ColorByte(r, g, b, a);
    }
    
    public Vector2 ReadVec2()
    {
        float x = Reader.ReadSingle();
        float y = Reader.ReadSingle();
        return new Vector2(x, y);
    }
    
    public Vector3 ReadVec3()
    {
        float x = Reader.ReadSingle();
        float y = Reader.ReadSingle();
        float z = Reader.ReadSingle();
        return new Vector3(x, y, z);
    }
    
    public Vector4 ReadVec4()
    {
        float x = Reader.ReadSingle();
        float y = Reader.ReadSingle();
        float z = Reader.ReadSingle();
        float w = Reader.ReadSingle();
        return new Vector4(x, y, z, w);
    }
}