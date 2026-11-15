using System.Numerics;
using KSP_PBR_Patcher.Model.Components;
using KSP_PBR_Patcher.Model.Components.Collider;
using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model;

public class MuTransform
{
    public required string Name { get; set; }
    public Vector3 Position { get; set; } =  new Vector3(0, 0, 0);
    public Vector4 Rotation { get; set; } =  new Vector4(0, 0, 0, 1);
    public Vector3 Scale { get; set; } = new Vector3(1, 1, 1);
    public Dictionary<MuTag, IMuComponent> Data { get; set; } = [];
    public List<MuTransform> Children { get; set; } = [];

    public IMuComponent this[MuTag tag] => Data[tag];

    public override string ToString()
    {
        return Name;
    }

    public static MuTransform Read(MuReader reader)
    {
        string name = reader.ReadString();
        Vector3 pos = reader.ReadVec3();
        Vector4 rot = reader.ReadVec4();
        Vector3 scale = reader.ReadVec3();

        Dictionary<MuTag, IMuComponent> data = new();
        List<MuTransform> children = [];
        
        if (reader.Version <= 2)
        {
            reader.ReadSingle(); // Skip unknown value
        }

        bool loop = true;
        while (loop)
        {
            try
            {
                MuTag tag = reader.ReadTag();

                switch (tag)
                {
                    case MuTag.ChildTransformStart:
                        // Don't error if not a tag, just keep going
                        if (reader.ReadInt32() == (int)MuTag.ChildTransformEnd)
                        {
                            loop = false;
                            break;
                        }

                        reader.Rewind(4);

                        MuTransform childTransform = Read(reader);
                        children.Add(childTransform);
                        break;
                    case MuTag.ChildTransformEnd:
                        loop = false;
                        break;
                    
                    case MuTag.UnityInfo:
                        data[tag] = MuComponentUnityInfo.Read(reader);
                        break;
                    
                    case MuTag.MeshFilter:
                        data[tag] = MuComponentMesh.Read(reader);
                        break;
                    case MuTag.MeshRenderer:
                        data[tag] = MuComponentRenderer.Read(reader);
                        break;
                    
                    case MuTag.ColliderBox:
                        data[tag] = MuComponentColliderBox.Read(reader, false);
                        break;
                    case MuTag.ColliderBox2:
                        data[tag] = MuComponentColliderBox.Read(reader, true);
                        break;
                    case MuTag.ColliderSphere:
                        data[tag] = MuComponentColliderSphere.Read(reader, false);
                        break;
                    case MuTag.ColliderSphere2:
                        data[tag] = MuComponentColliderSphere.Read(reader, true);
                        break;
                    case MuTag.ColliderCapsule:
                        data[tag] = MuComponentColliderCapsule.Read(reader, false);
                        break;
                    case MuTag.ColliderCapsule2:
                        data[tag] = MuComponentColliderCapsule.Read(reader, true);
                        break;
                    case MuTag.ColliderMesh:
                        data[tag] = MuComponentColliderMesh.Read(reader, false);
                        break;
                    case MuTag.ColliderMesh2:
                        data[tag] = MuComponentColliderMesh.Read(reader, true);
                        break;
                    case MuTag.ColliderWheel:
                        data[tag] = MuComponentColliderWheel.Read(reader);
                        break;
                    
                    case MuTag.Animation:
                        data[tag] = MuComponentAnimation.Read(reader);
                        break;
                    case MuTag.SkinnedMeshRenderer:
                        data[tag] = MuComponentSkinnedMesh.Read(reader);
                        break;
                    case MuTag.Light:
                        data[tag] = MuComponentLight.Read(reader);
                        break;
                    case MuTag.Particles:
                        data[tag] = MuComponentParticles.Read(reader);
                        break;
                    
                    case MuTag.Materials:
                        reader.Rewind(4);
                        loop = false;
                        break;
                    
                    default:
                        throw new ArgumentException($"Unknown tag {tag}");
                }
            }
            catch (EndOfStreamException)
            {
                break;
            }
        }

        return new MuTransform
        {
            Name = name,
            Position = pos,
            Rotation = rot,
            Scale = scale,
            Data = data,
            Children = children,
        };
    }

    public void Write(BinaryWriter writer)
    {
        writer.Write(Name);

        writer.Write(Position);
        writer.Write(Rotation);
        writer.Write(Scale);

        foreach ((MuTag tag, IMuComponent component) in Data)
        {
            component.Write(writer);
        }
        
        foreach (MuTransform child in Children)
        {
            writer.Write(MuTag.ChildTransformStart);
            child.Write(writer);
            writer.Write(MuTag.ChildTransformEnd);
        }
    }

    public int GetMaterialIndex()
    {
        if (Data.TryGetValue(MuTag.MeshRenderer, out IMuComponent? value))
        {
            MuComponentRenderer renderer = (MuComponentRenderer)value;
            return renderer.MaterialIndex;
        }

        if (Data.TryGetValue(MuTag.SkinnedMeshRenderer, out IMuComponent? value1))
        {
            MuComponentSkinnedMesh skinnedMesh = (MuComponentSkinnedMesh)value1;
            return skinnedMesh.MaterialIndices[0]; // TODO - Should this be smarter?
        }

        throw new KeyNotFoundException($"Cannot get material index of transform {Name}: it has no renderable components");
    }

    public void SetMaterialIndex(int newMaterialIndex)
    {
        if (Data.TryGetValue(MuTag.MeshRenderer, out IMuComponent? value))
        {
            MuComponentRenderer renderer = (MuComponentRenderer)value;
            renderer.MaterialIndex = newMaterialIndex;
            return;
        }

        if (Data.TryGetValue(MuTag.SkinnedMeshRenderer, out IMuComponent? value1))
        {
            MuComponentSkinnedMesh skinnedMesh = (MuComponentSkinnedMesh)value1;
            skinnedMesh.MaterialIndices[0] = newMaterialIndex; // TODO - Should this be smarter?
            return;
        }

        throw new KeyNotFoundException($"Cannot get material index of transform {Name}: it has no renderable components");
    }

    public MuTransform Clone()
    {
        return new MuTransform
        {
            Name = Name,
            Position = Position,
            Rotation = Rotation,
            Scale = Scale,
            Data = Data.ToDictionary(pair => pair.Key, pair => pair.Value.Clone()),
            Children = Children.Select(child => child.Clone()).ToList(),
        };
    }
}