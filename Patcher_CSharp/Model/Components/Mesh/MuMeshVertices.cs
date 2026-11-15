using System.Numerics;
using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model.Components.Mesh;

public class MuMeshVertices : IMuMeshComponent
{
    public required Vector3[] Vertices { get; set; }

    public static MuMeshVertices Read(MuReader reader, int numVertices)
    {
        Vector3[] vertices = new Vector3[numVertices];
        for (int i = 0; i < vertices.Length; i++)
        {
            vertices[i] = reader.ReadVec3();
        }

        return new MuMeshVertices
        {
            Vertices = vertices
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.MeshVertices);

        foreach (Vector3 vertex in Vertices)
        {
            writer.Write(vertex);
        }
    }

    public void Delete(HashSet<int> indices)
    {
        Vector3[] verticesNew = new Vector3[Vertices.Length - indices.Count];
        int index = 0;
        for (int i = 0; i < Vertices.Length; i++)
        {
            if (indices.Contains(i))
            {
                continue;
            }

            verticesNew[index] = Vertices[i];
            index++;
        }
        
        Vertices = verticesNew;
    }

    public void Paste(MuMeshVertices vertices)
    {
        Vector3[] verticesNew = new Vector3[Vertices.Length + vertices.Vertices.Length];
        for (int i = 0; i < Vertices.Length; i++)
        {
            verticesNew[i] = Vertices[i];
        }

        for (int i = 0; i < vertices.Vertices.Length; i++)
        {
            verticesNew[i + Vertices.Length] = vertices.Vertices[i];
        }
        
        Vertices = verticesNew;
    }
}