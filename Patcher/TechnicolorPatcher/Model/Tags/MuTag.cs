namespace TechnicolorPatcher.Model.Tags;

public enum MuTag
{
    Invalid = -1,
    UnityInfo = 0x18,
    
    ChildTransformStart = 0,
    ChildTransformEnd = 1,

    ColliderBox = 6,
    ColliderBox2 = 0x1C,
    ColliderSphere = 4,
    ColliderSphere2 = 0x1A,
    ColliderCapsule = 5,
    ColliderCapsule2 = 0x1B,
    ColliderMesh = 3,
    ColliderMesh2 = 0x19,
    ColliderWheel = 0x1D,

    Animation = 2,
    SkinnedMeshRenderer = 9,

    MeshFilter = 7,
    MeshStart = 0xD,
    MeshVertices = 0xE,
    MeshUv = 0xF,
    MeshUv2 = 0x10,
    MeshNormals = 0x11,
    MeshTangents = 0x12,
    MeshTriangles = 0x13,
    MeshBoneWeights = 0x14,
    MeshBindPoses = 0x15,
    MeshVertexColors = 0x20,
    MeshEnd = 0x16,
    MeshRenderer = 8,

    Light = 0x17,
    Camera = 0x1E,
    Particles = 0x1F,

    Materials = 0xA,
    Material = 0xB,
    Textures = 0xC,
}