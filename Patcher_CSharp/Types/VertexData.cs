using System.Numerics;

namespace KSP_PBR_Patcher.Types;

public class VertexData
{
    public Vector3 Position { get; set; }
    public Vector2? Uv { get; set; }
    public Vector2? Uv2 { get; set; }
    public Vector3? Normal { get; set; }
    public Vector4? Tangent { get; set; }
    public ColorByte? VertexColor { get; set; }
    public BoneWeight? BoneWeight { get; set; }

    public VertexData Clone()
    {
        return new VertexData
        {
            Position = Position,
            Uv = Uv,
            Uv2 = Uv2,
            Normal = Normal,
            Tangent = Tangent,
            VertexColor = VertexColor,
            BoneWeight = BoneWeight
        };
    }
}