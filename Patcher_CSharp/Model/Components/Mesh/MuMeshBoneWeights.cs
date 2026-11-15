using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;
using KSP_PBR_Patcher.Types;

namespace KSP_PBR_Patcher.Model.Components.Mesh;

public class MuMeshBoneWeights : IMuMeshComponent
{
    public required BoneWeight[] BoneWeights { get; set; }

    public static MuMeshBoneWeights Read(MuReader reader, int numVertices)
    {
        BoneWeight[] boneWeights = new BoneWeight[numVertices];
        for (int i = 0; i < boneWeights.Length; i++)
        {
            boneWeights[i] = reader.ReadBoneWeight();
        }

        return new MuMeshBoneWeights
        {
            BoneWeights = boneWeights
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.MeshBoneWeights);

        foreach (BoneWeight boneWeight in BoneWeights)
        {
            writer.Write(boneWeight);
        }
    }

    public void Delete(HashSet<int> indices)
    {
        BoneWeight[] boneWeightsNew = new BoneWeight[BoneWeights.Length - indices.Count];
        int index = 0;
        for (int i = 0; i < BoneWeights.Length; i++)
        {
            if (indices.Contains(i))
            {
                continue;
            }

            boneWeightsNew[index] = BoneWeights[i];
            index++;
        }
        
        BoneWeights = boneWeightsNew;
    }

    public void Paste(MuMeshBoneWeights vertices)
    {
        BoneWeight[] boneWeightsNew = new BoneWeight[BoneWeights.Length + vertices.BoneWeights.Length];
        for (int i = 0; i < BoneWeights.Length; i++)
        {
            boneWeightsNew[i] = BoneWeights[i];
        }

        for (int i = 0; i < vertices.BoneWeights.Length; i++)
        {
            boneWeightsNew[i + BoneWeights.Length] = vertices.BoneWeights[i];
        }
        
        BoneWeights = boneWeightsNew;
    }
}