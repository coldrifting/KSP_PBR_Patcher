using System.Numerics;
using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model.Components.Mesh;

public class MuMeshUvs : IMuMeshComponent
{
    public required Vector2[] Uvs { get; set; }
    public bool IsUv2 { get; set; }
    
    public static MuMeshUvs Read(MuReader reader, int numVertices, bool isUv2)
    {
        Vector2[] uvs = new Vector2[numVertices];

        for (int i = 0; i < uvs.Length; i++)
        {
            uvs[i] = reader.ReadVec2();
        }

        return new MuMeshUvs
        {
            Uvs = uvs,
            IsUv2 = isUv2
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(IsUv2 ? MuTag.MeshUv2 : MuTag.MeshUv);

        foreach (Vector2 vertexColor in Uvs)
        {
            writer.Write(vertexColor);
        }
    }

    public void Delete(HashSet<int> indices)
    {
        Vector2[] uvsNew = new Vector2[Uvs.Length - indices.Count];
        int index = 0;
        for (int i = 0; i < Uvs.Length; i++)
        {
            if (indices.Contains(i))
            {
                continue;
            }

            uvsNew[index] = Uvs[i];
            index++;
        }
        
        Uvs = uvsNew;
    }

    public void Paste(MuMeshUvs vertices)
    {
        Vector2[] uvsNew = new Vector2[Uvs.Length + vertices.Uvs.Length];
        for (int i = 0; i < Uvs.Length; i++)
        {
            uvsNew[i] = Uvs[i];
        }

        for (int i = 0; i < vertices.Uvs.Length; i++)
        {
            uvsNew[i + Uvs.Length] = vertices.Uvs[i];
        }
        
        Uvs = uvsNew;
    }
}