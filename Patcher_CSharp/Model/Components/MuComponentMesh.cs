using System.Numerics;
using KSP_PBR_Patcher.Model.Components.Mesh;
using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;
using KSP_PBR_Patcher.Types;

namespace KSP_PBR_Patcher.Model.Components;

public class MuComponentMesh : IMuComponent
{
    public int NumSubMeshes { get; set; }
    public required List<MuTag> Ordering { get; set; }
    public required VertexData[] VertexData { get; set; }
    public required Int3[] Triangles { get; set; }
    public required MuMeshBindPoses? BindPoses { get; set; }
    public bool HasFilter { get; set; }

    public static MuComponentMesh Read(MuReader reader)
    {
        MuTag tag = reader.ReadTag();
        if (tag != MuTag.MeshStart)
        {
            throw new Exception($"Invalid Mu Tag for MuMesh: \n{tag}");
        }

        int numVertices = reader.ReadInt32();
        int numSubMeshes = reader.ReadInt32();

        Dictionary<MuTag, IMuMeshComponent> data = new();

        List<MuTag> ordering = [];

        bool loop = true;
        while (loop)
        {
            tag = reader.ReadTag();
            switch (tag)
            {
                case MuTag.MeshVertices:
                    data[tag] = MuMeshVertices.Read(reader, numVertices);
                    ordering.Add(tag);
                    break;
                case MuTag.MeshUv:
                    data[tag] = MuMeshUvs.Read(reader, numVertices, false);
                    ordering.Add(tag);
                    break;
                case MuTag.MeshUv2:
                    data[tag] = MuMeshUvs.Read(reader, numVertices, true);
                    ordering.Add(tag);
                    break;
                case MuTag.MeshNormals:
                    data[tag] = MuMeshNormals.Read(reader, numVertices);
                    ordering.Add(tag);
                    break;
                case MuTag.MeshTangents:
                    data[tag] = MuMeshTangents.Read(reader, numVertices);
                    ordering.Add(tag);
                    break;
                case MuTag.MeshBoneWeights:
                    data[tag] = MuMeshBoneWeights.Read(reader, numVertices);
                    ordering.Add(tag);
                    break;
                case MuTag.MeshVertexColors:
                    data[tag] = MuMeshVertexColors.Read(reader, numVertices);
                    ordering.Add(tag);
                    break;
                case MuTag.MeshTriangles:
                    data[tag] = MuMeshTriangles.Read(reader);
                    ordering.Add(tag);
                    break;
                case MuTag.MeshBindPoses:
                    data[tag] = MuMeshBindPoses.Read(reader);
                    ordering.Add(tag);
                    break;
                case MuTag.MeshEnd:
                    loop = false;
                    break;
                
                case MuTag.Invalid:
                case MuTag.UnityInfo:
                case MuTag.ChildTransformStart:
                case MuTag.ChildTransformEnd:
                case MuTag.ColliderBox:
                case MuTag.ColliderBox2:
                case MuTag.ColliderSphere:
                case MuTag.ColliderSphere2:
                case MuTag.ColliderCapsule:
                case MuTag.ColliderCapsule2:
                case MuTag.ColliderMesh:
                case MuTag.ColliderMesh2:
                case MuTag.ColliderWheel:
                case MuTag.Animation:
                case MuTag.SkinnedMeshRenderer:
                case MuTag.MeshFilter:
                case MuTag.MeshStart:
                case MuTag.MeshRenderer:
                case MuTag.Light:
                case MuTag.Camera:
                case MuTag.Particles:
                case MuTag.Materials:
                case MuTag.Material:
                case MuTag.Textures:
                default:
                    throw new InvalidDataException($"Unexpected tag in mesh data: \n{tag}");
            }
        }

        if (!data.TryGetValue(MuTag.MeshVertices, out IMuMeshComponent? vertices))
        {
            throw new InvalidDataException("No vertices found for mesh");
        }

        if (!data.TryGetValue(MuTag.MeshTriangles, out IMuMeshComponent? triangles))
        {
            throw new InvalidDataException("No triangles found for mesh");
        }

        MuMeshBindPoses? poses = data.TryGetValue(MuTag.MeshBindPoses, out IMuMeshComponent? poseOut) ? (MuMeshBindPoses)poseOut : null;
        
        MuMeshUvs? uvs = data.TryGetValue(MuTag.MeshUv, out IMuMeshComponent? uvOut) ? (MuMeshUvs)uvOut : null;
        MuMeshUvs? uvs2 = data.TryGetValue(MuTag.MeshUv2, out IMuMeshComponent? uv2Out) ? (MuMeshUvs)uv2Out : null;
        MuMeshNormals? normals = data.TryGetValue(MuTag.MeshNormals, out IMuMeshComponent? normalOut) ? (MuMeshNormals)normalOut : null;
        MuMeshTangents? tangents = data.TryGetValue(MuTag.MeshTangents, out IMuMeshComponent? tangentOut) ? (MuMeshTangents)tangentOut : null;
        MuMeshVertexColors? vertexColors = data.TryGetValue(MuTag.MeshVertexColors, out IMuMeshComponent? vertexColorOut) ? (MuMeshVertexColors)vertexColorOut : null;
        MuMeshBoneWeights? boneWeights = data.TryGetValue(MuTag.MeshBoneWeights, out IMuMeshComponent? boneWeightOut) ? (MuMeshBoneWeights)boneWeightOut : null;

        VertexData[] vertexData = new VertexData[numVertices];
        
        for (int i = 0; i < numVertices; i++)
        {
            VertexData vData = new()
            {
                Position = ((MuMeshVertices)vertices).Vertices[i],
                Uv = uvs?.Uvs[i],
                Uv2 = uvs2?.Uvs[i],
                Normal = normals?.Normals[i],
                Tangent = tangents?.Tangents[i],
                VertexColor = vertexColors?.VertexColors[i],
                BoneWeight = boneWeights?.BoneWeights[i],
            };

            vertexData[i] = vData;
        }

        return new MuComponentMesh
        {
            NumSubMeshes = numSubMeshes,
            Ordering = ordering,
            VertexData = vertexData,
            Triangles = ((MuMeshTriangles)triangles).Triangles,
            BindPoses = poses,
            HasFilter = true
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        if (HasFilter)
        {
            writer.Write(MuTag.MeshFilter);
        }

        writer.Write(MuTag.MeshStart);

        writer.Write(VertexData.Length);
        writer.Write(NumSubMeshes);

        Vector3[] verts = new Vector3[VertexData.Length];
        Vector2[] uvs = new Vector2[VertexData.Length];
        Vector2[] uvs2 = new Vector2[VertexData.Length];
        Vector3[] normals = new Vector3[VertexData.Length];
        Vector4[] tangents = new Vector4[VertexData.Length];
        ColorByte[] vertexColors = new ColorByte[VertexData.Length];
        BoneWeight[] boneWeights = new BoneWeight[VertexData.Length];

        for (int i = 0; i < VertexData.Length; i++)
        {
            VertexData dataPoint = VertexData[i];
            verts[i] = dataPoint.Position;

            if (dataPoint.Uv is not null)
            {
                uvs[i] = dataPoint.Uv.Value;
            }

            if (dataPoint.Uv2 is not null)
            {
                uvs2[i] = dataPoint.Uv2.Value;
            }

            if (dataPoint.Normal is not null)
            {
                normals[i] = dataPoint.Normal.Value;
            }

            if (dataPoint.Tangent is not null)
            {
                tangents[i] = dataPoint.Tangent.Value;
            }

            if (dataPoint.VertexColor is not null)
            {
                vertexColors[i] = dataPoint.VertexColor.Value;
            }

            if (dataPoint.BoneWeight is not null)
            {
                boneWeights[i] = dataPoint.BoneWeight.Value;
            }
        }

        Dictionary<MuTag, IMuMeshComponent> data = new Dictionary<MuTag, IMuMeshComponent>();
        foreach (MuTag tag in Ordering)
        {
            switch (tag)
            {
                case MuTag.MeshVertices:
                    data[tag] = new MuMeshVertices
                    {
                        Vertices = verts,
                    };
                    break;
                case MuTag.MeshUv:
                    data[tag] = new MuMeshUvs
                    {
                        Uvs = uvs,
                        IsUv2 = false,
                    };
                    break;
                case MuTag.MeshUv2:
                    data[tag] = new MuMeshUvs
                    {
                        Uvs = uvs2,
                        IsUv2 = true,
                    };
                    break;
                case MuTag.MeshNormals:
                    data[tag] = new MuMeshNormals
                    {
                        Normals = normals,
                    };
                    break;
                case MuTag.MeshTangents:
                    data[tag] = new MuMeshTangents
                    {
                        Tangents = tangents,
                    };
                    break;
                case MuTag.MeshVertexColors:
                    data[tag] = new MuMeshVertexColors
                    {
                        VertexColors = vertexColors,
                    };
                    break;
                case MuTag.MeshBoneWeights:
                    data[tag] = new MuMeshBoneWeights
                    {
                        BoneWeights = boneWeights,
                    };
                    break;
                case MuTag.MeshBindPoses:
                    if (BindPoses is not null)
                    {
                        data[tag] = BindPoses;
                    }

                    break;
                case MuTag.MeshTriangles:
                    data[tag] = new MuMeshTriangles
                    {
                        Triangles = Triangles,
                    };
                    break;
            }
        }
        
        foreach (MuTag tag in Ordering)
        {
            IMuMeshComponent item = data[tag];
            switch (item)
            {
                case MuMeshBindPoses muMeshBindPoses:
                    muMeshBindPoses.Write(writer);
                    break;
                case MuMeshBoneWeights muMeshBoneWeights:
                    muMeshBoneWeights.Write(writer);
                    break;
                case MuMeshNormals muMeshNormals:
                    muMeshNormals.Write(writer);
                    break;
                case MuMeshTangents muMeshTangents:
                    muMeshTangents.Write(writer);
                    break;
                case MuMeshVertices meshVertices:
                    meshVertices.Write(writer);
                    break;
                case MuMeshTriangles meshTriangles:
                    meshTriangles.Write(writer);
                    break;
                case MuMeshUvs muMeshUvs:
                    muMeshUvs.Write(writer);
                    break;
                case MuMeshVertexColors muMeshVertexColors:
                    muMeshVertexColors.Write(writer);
                    break;
            }
        }
        
        writer.Write(MuTag.MeshEnd);
    }

    public IMuComponent Clone()
    {
        return new MuComponentMesh
        {
            NumSubMeshes = NumSubMeshes,
            Ordering = Ordering.Select(o => o).ToList(),
            VertexData = VertexData.Select(v => v.Clone()).ToArray(),
            Triangles = Triangles.Select(t => t).ToArray(),
            BindPoses = BindPoses,
            HasFilter = HasFilter
        };
    }
}