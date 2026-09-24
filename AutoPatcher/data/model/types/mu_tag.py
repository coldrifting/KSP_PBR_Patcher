from enum import IntEnum


class MuTag(IntEnum):
    Invalid = -1
    UnityTagAndLayer = 24 # 0x18

    ChildTransformStart = 0
    ChildTransformEnd = 1

    BoxCollider = 6
    BoxCollider2 = 28 # 0x1C
    SphereCollider = 4
    SphereCollider2 = 26 # 0x1A
    CapsuleCollider = 5
    CapsuleCollider2 = 27 # 0x1B
    MeshCollider = 3
    MeshCollider2 = 25 # 0x19
    WheelCollider = 29 # 0x1D

    Animation = 2
    SkinnedMeshRenderer = 9

    MeshFilter = 7
    MeshStart = 13 # 0xD
    MeshVertices = 14 # 0xE
    MeshUv = 15 # 0xF
    MeshUv2 = 16 # 0x10
    MeshNormals = 17 # 0x11
    MeshTangents = 18 # 0x12
    MeshTriangles = 19 # 0x13
    MeshBoneWeights = 20 # 0x14
    MeshBindPoses = 21 # 0x15
    MeshVertexColors = 32 # 0x20
    MeshEnd = 22 # 0x16
    MeshRenderer = 8

    Light = 23 # 0x17
    Camera = 30 # 0x1E
    Particles = 31 # 0x1F

    Materials = 10 # 0xA
    Material = 11 # 0xB
    Textures = 12 # 0xC