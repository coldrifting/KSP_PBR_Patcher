using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;
using KSP_PBR_Patcher.Types;

namespace KSP_PBR_Patcher.Model.Components.Mesh;

public class MuMeshVertexColors : IMuMeshComponent
{
    public required ColorByte[] VertexColors { get; set; }
    
    public static MuMeshVertexColors Read(MuReader reader, int numVertices)
    {
        ColorByte[] vertexColors = new ColorByte[numVertices];

        for (int i = 0; i < vertexColors.Length; i++)
        {
            vertexColors[i] = reader.ReadColorByte();
        }

        return new MuMeshVertexColors
        {
            VertexColors = vertexColors
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.MeshVertexColors);

        foreach (ColorByte vertexColor in VertexColors)
        {
            writer.Write(vertexColor);
        }
    }

    public void Delete(HashSet<int> indices)
    {
        ColorByte[] vertexColorsNew = new ColorByte[VertexColors.Length - indices.Count];
        int index = 0;
        for (int i = 0; i < VertexColors.Length; i++)
        {
            if (indices.Contains(i))
            {
                continue;
            }

            vertexColorsNew[index] = VertexColors[i];
            index++;
        }
        
        VertexColors = vertexColorsNew;
    }

    public void Paste(MuMeshVertexColors vertices)
    {
        ColorByte[] vertexColorsNew = new ColorByte[VertexColors.Length + vertices.VertexColors.Length];
        for (int i = 0; i < VertexColors.Length; i++)
        {
            vertexColorsNew[i] = VertexColors[i];
        }

        for (int i = 0; i < vertices.VertexColors.Length; i++)
        {
            vertexColorsNew[i + VertexColors.Length] = vertices.VertexColors[i];
        }
        
        VertexColors = vertexColorsNew;
    }
}