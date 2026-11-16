using System.Text;
using TechnicolorPatcher.Model.Components.Material;
using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;

namespace TechnicolorPatcher.Model;

public class MuFile
{
    public required string Name { get; set; }
    public required MuTransform RootTransform { get; set; }
    public List<Material> Materials { get; set; } = [];
    public List<Texture> Textures { get; set; } = [];

    public static MuFile ReadFile(string path)
    {
        MuReader reader = new MuReader(path);
        MuFile file = Read(reader);
        return file;
    }
    
    public static MuFile Read(MuReader reader)
    {
        string name = reader.ReadString();
        MuTransform root = MuTransform.Read(reader);
        
        Material[] materials;
        try
        {
            MuTag matTag = reader.ReadTag();
            if (matTag != MuTag.Materials)
            {
                throw new InvalidDataException($"Expected {MuTag.Materials}, but got {matTag}");
            }
            
            int numMaterials = reader.ReadInt32();
            materials = new Material[numMaterials];
            for (int i = 0; i < materials.Length; i++)
            {
                Material material = Material.Read(reader);
                materials[i] = material;
            }
        }
        catch (EndOfStreamException)
        {
            materials = [];
        }

        Texture[] textures;
        try
        {
            MuTag texTag = reader.ReadTag();
            if (texTag != MuTag.Textures)
            {
                throw new InvalidDataException($"Expected {MuTag.Textures}, but got {texTag}");
            }

            int numTextures = reader.ReadInt32();
            textures = new Texture[numTextures];
            for (int i = 0; i < textures.Length; i++)
            {
                Texture texture = Texture.Read(reader);
                textures[i] = texture;
            }
        }
        catch (EndOfStreamException)
        {
            textures = [];
        }

        return new MuFile
        {
            Name = name,
            RootTransform = root,
            Materials = materials.ToList(),
            Textures = textures.ToList()
        };
    }

    public void WriteFile(string path)
    {
        using FileStream stream = File.Open(path, FileMode.Create);
        using BinaryWriter writer = new(stream, Encoding.UTF8, false);
        Write(writer);
    }

    public void Write(BinaryWriter writer)
    {
        writer.Write(MuReader.MagicNumber);
        writer.Write(5); // Mu File Version 5.0
        writer.Write(Name);
        RootTransform.Write(writer);

        if (Materials.Count > 0)
        {
            writer.Write(MuTag.Materials);
            writer.Write(Materials.Count);
            foreach (Material material in Materials)
            {
                material.Write(writer);
            }
        }
        
        if (Textures.Count > 0) {
            writer.Write(MuTag.Textures);
            writer.Write(Textures.Count);
            foreach (Texture texture in Textures)
            {
                texture.Write(writer);
            }
        }
    }
}