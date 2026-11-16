using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;
using TechnicolorPatcher.Types;

namespace TechnicolorPatcher.Model.Components.Mesh;

public class MuMeshTriangles : IMuMeshComponent
{
    public required Int3[] Triangles { get; set; }

    public static MuMeshTriangles Read(MuReader reader)
    {
        int numTriangles = reader.ReadInt32() / 3;
        Int3[] triangles = new Int3[numTriangles];
        for (int i = 0; i < triangles.Length; i++)
        {
            triangles[i] = reader.ReadInt3();
        }

        return new MuMeshTriangles
        {
            Triangles = triangles
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.MeshTriangles);

        writer.Write(Triangles.Length * 3);
        foreach (Int3 triangle in Triangles)
        {
            writer.Write(triangle);
        }
    }

    public void Delete(HashSet<int> indices)
    {
        Int3[] trianglesNew = new Int3[Triangles.Length - indices.Count];
        int index = 0;
        for (int i = 0; i < Triangles.Length; i++)
        {
            if (indices.Contains(i))
            {
                continue;
            }

            trianglesNew[index] = Triangles[i];
            index++;
        }
        
        Triangles = trianglesNew;
    }

    public void Paste(MuMeshTriangles vertices)
    {
        Int3[] trianglesNew = new Int3[Triangles.Length + vertices.Triangles.Length];
        for (int i = 0; i < Triangles.Length; i++)
        {
            trianglesNew[i] = Triangles[i];
        }

        for (int i = 0; i < vertices.Triangles.Length; i++)
        {
            trianglesNew[i + Triangles.Length] = vertices.Triangles[i];
        }
        
        Triangles = trianglesNew;
    }
}