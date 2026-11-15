using KSP_PBR_Patcher.Model.Components.Material;
using KSP_PBR_Patcher.Model.ModelOperations;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace KSP_PBR_Patcher.Model.Config;

public class ConfigModel
{
    public required string Model { get; set; }
    public required OperationBase[] Operations { get; set; } = [];
    public required Dictionary<string, ColorZone> ColorZones { get; set; } = [];

    public static ConfigModel Load(string path)
    {
        string configText = File.ReadAllText(path);
        IDeserializer deserializer = new DeserializerBuilder()
            .WithNamingConvention(UnderscoredNamingConvention.Instance)
            .Build();
        
        ConfigModel configModel = deserializer.Deserialize<ConfigModel>(configText);
        return configModel;
    }

    public void Apply(string gameDataPath, string outputAssetPath) 
    {
        if (Operations.Length == 0 && ColorZones.Count == 0)
        {
            Console.Error.WriteLine($"Model File {Model} has no operations or color zones defined");
            return;
        }

        string sourceFile = Path.Combine(gameDataPath, Model) + ".mu";
        if (!File.Exists(sourceFile))
        {
            throw new FileNotFoundException($"Unable to find the file {sourceFile}. Does it exist?");
        }
        
        MuFile muFile = MuFile.ReadFile(sourceFile);
        foreach (OperationBase operation in Operations)
        {
            operation.Apply(muFile, gameDataPath);
        }

        if (ColorZones.Count > 0)
        {
            ColorZone.ApplyColorZones(muFile, ColorZones);
        }

        string outputFile = Path.Combine(outputAssetPath, Path.GetFileName(Model)) + ".mu";
        string? parentPath = Path.GetDirectoryName(outputFile);
        if (parentPath is null)
        {
            throw new ArgumentException("Output Parent path is null");
        }
        
        if (!Directory.Exists(parentPath))
        {
            Directory.CreateDirectory(parentPath);
        }

        muFile.WriteFile(outputFile);
        
        // Copy Textures
        foreach (Texture texture in muFile.Textures)
        {
            string? sourceFolder = Path.GetDirectoryName(sourceFile);
            if (sourceFolder is null)
            {
                throw new ArgumentException("Source Parent path is null");
            }

            string textureSource = Path.Combine(sourceFolder, Path.GetFileNameWithoutExtension(texture.Name)) + ".dds";
            if (!File.Exists(textureSource))
            {
                continue;
            }
            
            string textureDest = Path.Combine(parentPath, Path.GetFileNameWithoutExtension(texture.Name)) + ".dds";
            File.Copy(textureSource, textureDest, true);
        }
        
        // Copy textures from different folders
        foreach (OperationBase operation in Operations)
        {
            if (operation is not OperationEditMaterialTextures materials)
            {
                continue;
            }

            CopyTexture(gameDataPath, parentPath, materials.MainTex);
            CopyTexture(gameDataPath, parentPath, materials.BumpMap);
            CopyTexture(gameDataPath, parentPath, materials.Emissive);
            CopyTexture(gameDataPath, parentPath, materials.MetalMap);
            CopyTexture(gameDataPath, parentPath, materials.TeamColorMap);
        }
    }

    private void CopyTexture(string gameDataPath, string outputFolder, string? texturePath)
    {
        if (texturePath is null)
        {
            return;
        }
        
        string sourceTex = Path.Combine(gameDataPath, texturePath) + ".dds";
        if (!File.Exists(sourceTex))
        {
            if (sourceTex.EndsWith("-a.dds"))
            {
                // Ignore preconverted textures
                return;
            }
            
            throw new FileNotFoundException($"Unable to find texture file: \n{sourceTex}");
        }
        
        string destTex = Path.Combine(outputFolder, Path.GetFileName(texturePath)) + ".dds";

        if (!File.Exists(destTex))
        {
            File.Copy(sourceTex, destTex, true);
        }
    }

    public static ConfigModel FromYaml(string yaml)
    {
        IDeserializer deserializer = new DeserializerBuilder()
            .WithNamingConvention(UnderscoredNamingConvention.Instance)
            .WithNodeDeserializer(new OperationDeserializer())
            .Build();
        
        ConfigModel configModel = deserializer.Deserialize<ConfigModel>(yaml);

        return configModel;
    }
}