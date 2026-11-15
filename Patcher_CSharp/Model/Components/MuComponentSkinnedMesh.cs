using System.Numerics;
using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model.Components;

public class MuComponentSkinnedMesh : IMuComponent
{
    public required int[] MaterialIndices { get; set; }
    public Vector3 Center { get; set; }
    public Vector3 Size { get; set; }
    public int Quality { get; set; }
    public bool UpdateWhenOffscreen { get; set; }
    public required string[] BoneNames { get; set; }
    public required MuComponentMesh Mesh { get; set; }

    public static MuComponentSkinnedMesh Read(MuReader reader)
    {
        int numMaterialIndices = reader.ReadInt32();
        int[] materialIndices = new int[numMaterialIndices];
        for (int i = 0; i < materialIndices.Length; i++)
        {
            materialIndices[i] = reader.ReadInt32();
        }

        Vector3 center = reader.ReadVec3();
        Vector3 size = reader.ReadVec3();
        int quality = reader.ReadInt32();
        bool updateWhenOffscreen = reader.ReadBoolean();

        int numBoneNames = reader.ReadInt32();
        string[] boneNames = new string[numBoneNames];
        for (int i = 0; i < boneNames.Length; i++)
        {
            boneNames[i] = reader.ReadString();
        }

        MuComponentMesh mesh = MuComponentMesh.Read(reader);
        mesh.HasFilter = false;

        return new MuComponentSkinnedMesh
        {
            MaterialIndices = materialIndices,
            Center = center,
            Size = size,
            Quality = quality,
            UpdateWhenOffscreen = updateWhenOffscreen,
            BoneNames = boneNames,
            Mesh = mesh
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.SkinnedMeshRenderer);
        
        writer.Write(MaterialIndices);
        writer.Write(Center);
        writer.Write(Size);
        writer.Write(Quality);
        writer.Write(UpdateWhenOffscreen);
        writer.Write(BoneNames);
        Mesh.Write(writer);
    }

    public IMuComponent Clone()
    {
        return new MuComponentSkinnedMesh
        {
            MaterialIndices = MaterialIndices,
            Center = Center,
            Size = Size,
            Quality = Quality,
            UpdateWhenOffscreen = UpdateWhenOffscreen,
            BoneNames = BoneNames,
            Mesh = (MuComponentMesh)Mesh.Clone()
        };
    }
}