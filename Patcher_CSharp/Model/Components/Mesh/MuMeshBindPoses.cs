using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model.Components.Mesh;

public class MuMeshBindPoses : IMuMeshComponent
{
    public required int[] Poses { get; set; }

    public static MuMeshBindPoses Read(MuReader reader)
    {
        int numPoses = reader.ReadInt32() * 16;
        
        int[] poses = new int[numPoses];
        for (int i = 0; i < numPoses; i++)
        {
            poses[i] = reader.ReadInt32();
        }

        return new MuMeshBindPoses
        {
            Poses = poses
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.MeshBindPoses);
        
        writer.Write(Poses.Length / 16);

        foreach (int pose in Poses)
        {
            writer.Write(pose);
        }
    }
}