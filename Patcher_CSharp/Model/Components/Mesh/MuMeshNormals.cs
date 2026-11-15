using System.Numerics;
using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model.Components.Mesh;

public class MuMeshNormals : IMuMeshComponent
{
    public required Vector3[] Normals { get; set; }

    public static MuMeshNormals Read(MuReader reader, int numVertices)
    {
        Vector3[] normals = new Vector3[numVertices];
        for (int i = 0; i < normals.Length; i++)
        {
            normals[i] = reader.ReadVec3();
        }

        return new MuMeshNormals
        {
            Normals = normals
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.MeshNormals);

        foreach (Vector3 normal in Normals)
        {
            writer.Write(normal);
        }
    }

    public void Delete(HashSet<int> indices)
    {
        Vector3[] normalsNew = new Vector3[Normals.Length - indices.Count];
        int index = 0;
        for (int i = 0; i < Normals.Length; i++)
        {
            if (indices.Contains(i))
            {
                continue;
            }

            normalsNew[index] = Normals[i];
            index++;
        }
        
        Normals = normalsNew;
    }

    public void Paste(MuMeshNormals vertices)
    {
        Vector3[] normalsNew = new Vector3[Normals.Length + vertices.Normals.Length];
        for (int i = 0; i < Normals.Length; i++)
        {
            normalsNew[i] = Normals[i];
        }

        for (int i = 0; i < vertices.Normals.Length; i++)
        {
            normalsNew[i + Normals.Length] = vertices.Normals[i];
        }
        
        Normals = normalsNew;
    }
}