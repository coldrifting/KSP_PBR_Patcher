using System.Numerics;
using KSP_PBR_Patcher.Model.IO;

namespace KSP_PBR_Patcher.Model.Components.Animation;

public class MuAnimationClip
{
    public required string Name { get; set; }
    public Vector3 Center { get; set; }
    public Vector3 Size { get; set; }
    public int WrapMode { get; set; }
    public required MuAnimationCurve[] Curves { get; set; }

    public static MuAnimationClip Read(MuReader reader)
    {
        string name = reader.ReadString();
        Vector3 center = reader.ReadVec3();
        Vector3 size = reader.ReadVec3();
        int wrapMode = reader.ReadInt32();
       
        int numCurves = reader.ReadInt32();
        MuAnimationCurve[] curves = new MuAnimationCurve[numCurves];
        for (int i = 0; i < numCurves; i++)
        {
            curves[i] = MuAnimationCurve.Read(reader);
        }

        return new MuAnimationClip
        {
            Name = name,
            Center = center,
            Size = size,
            WrapMode = wrapMode,
            Curves = curves
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(Name);
        writer.Write(Center);
        writer.Write(Size);
        writer.Write(WrapMode);
        
        writer.Write(Curves.Length);
        foreach (MuAnimationCurve curve in Curves)
        {
            curve.Write(writer);
        }
    }

    public MuAnimationClip Clone()
    {
        return new MuAnimationClip
        {
            Name = Name,
            Center = Center,
            Size = Size,
            WrapMode = WrapMode,
            Curves = Curves.Select(c => c.Clone()).ToArray()
        };
    }
}