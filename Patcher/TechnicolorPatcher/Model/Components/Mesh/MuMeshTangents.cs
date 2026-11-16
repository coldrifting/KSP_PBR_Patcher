using TechnicolorPatcher.Types;
using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;

namespace TechnicolorPatcher.Model.Components.Mesh;

public class MuMeshTangents : IMuMeshComponent
{
    public required Vector4[] Tangents { get; set; }

    public static MuMeshTangents Read(MuReader reader, int numVertices)
    {
        Vector4[] tangents = new Vector4[numVertices];
        for (int i = 0; i < tangents.Length; i++)
        {
            tangents[i] = reader.ReadVec4();
        }

        return new MuMeshTangents
        {
            Tangents = tangents
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.MeshTangents);

        foreach (Vector4 tangent in Tangents)
        {
            writer.Write(tangent);
        }
    }

    public void Delete(HashSet<int> indices)
    {
        Vector4[] tangentsNew = new Vector4[Tangents.Length - indices.Count];
        int index = 0;
        for (int i = 0; i < Tangents.Length; i++)
        {
            if (indices.Contains(i))
            {
                continue;
            }

            tangentsNew[index] = Tangents[i];
            index++;
        }
        
        Tangents = tangentsNew;
    }

    public void Paste(MuMeshTangents vertices)
    {
        Vector4[] tangentsNew = new Vector4[Tangents.Length + vertices.Tangents.Length];
        for (int i = 0; i < Tangents.Length; i++)
        {
            tangentsNew[i] = Tangents[i];
        }

        for (int i = 0; i < vertices.Tangents.Length; i++)
        {
            tangentsNew[i + Tangents.Length] = vertices.Tangents[i];
        }
        
        Tangents = tangentsNew;
    }
}