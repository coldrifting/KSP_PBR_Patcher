using System.Numerics;
using KSP_PBR_Patcher.Model.Tags;
using KSP_PBR_Patcher.Types;

namespace KSP_PBR_Patcher.Model.IO;

public static class BinaryWriterExt
{
    public static void Write(this BinaryWriter writer, MuTag tag)
    {
        writer.Write((int)tag);
    }
    
    public static void Write(this BinaryWriter writer, int[] arr)
    {
        writer.Write(arr.Length);
        foreach (int s in arr)
        {
            writer.Write(s);
        }
    }
    
    public static void Write(this BinaryWriter writer, string[] arr)
    {
        writer.Write(arr.Length);
        foreach (string s in arr)
        {
            writer.Write(s);
        }
    }
    
    public static void Write(this BinaryWriter writer, BoneWeight boneWeight)
    {
        writer.Write(boneWeight.Indices);
        writer.Write(boneWeight.Weights);
    }
    
    public static void Write(this BinaryWriter writer, ColorByte colorByte)
    {
        writer.Write(colorByte.R);
        writer.Write(colorByte.G);
        writer.Write(colorByte.B);
        writer.Write(colorByte.A);
    }
    
    public static void Write(this BinaryWriter writer, Int3 int3)
    {
        writer.Write(int3.X);
        writer.Write(int3.Y);
        writer.Write(int3.Z);
    }
    
    public static void Write(this BinaryWriter writer, Int4 int4)
    {
        writer.Write(int4.X);
        writer.Write(int4.Y);
        writer.Write(int4.Z);
        writer.Write(int4.W);
    }
    
    public static void Write(this BinaryWriter writer, Vector2 vec2)
    {
        writer.Write(vec2.X);
        writer.Write(vec2.Y);
    }
    
    public static void Write(this BinaryWriter writer, Vector3 vec3)
    {
        writer.Write(vec3.X);
        writer.Write(vec3.Y);
        writer.Write(vec3.Z);
    }
    
    public static void Write(this BinaryWriter writer, Vector4 vec4)
    {
        writer.Write(vec4.X);
        writer.Write(vec4.Y);
        writer.Write(vec4.Z);
        writer.Write(vec4.W);
    }
}