using TechnicolorPatcher.Model.Components.Material;
using TechnicolorPatcher.Model.Operations;
using TechnicolorPatcher.Util;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace TechnicolorPatcher.Model.Config;

[YamlSerializable]
public class ConfigModel
{
    public required string Model { get; set; }
    public required OperationBase[]? Operations { get; set; } = [];
    public required Dictionary<string, ColorZone>? ColorZones { get; set; } = [];

    public void Apply(DirectoryInfo gameData, FileInfo outputFile) 
    {
        if (Operations is { Length: 0 } && ColorZones is { Count: 0 })
        {
            Console.Error.WriteLine($"Model File {Model} has no operations or color zones defined");
            return;
        }

        string sourceFile = Path.Combine(gameData.FullName, Model) + ".mu";
        if (!File.Exists(sourceFile))
        {
            throw new FileNotFoundException($"Unable to find the file {sourceFile}. Does it exist?");
        }
        
        MuFile muFile = MuFile.ReadFile(sourceFile);
        if (Operations is not null)
        {
            foreach (OperationBase operation in Operations)
            {
                operation.Apply(muFile, gameData.FullName);
            }
        }

        if (ColorZones is not null)
        {
            if (ColorZones.Count > 0)
            {
                ColorZone.ApplyColorZones(muFile, ColorZones);
            }
        }

        if (!outputFile.Directory!.Exists)
        {
            outputFile.Directory.Create();
        }

        muFile.WriteFile(outputFile.FullName);
        
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
            
            string textureDest = Path.Combine(outputFile.Directory.FullName, Path.GetFileNameWithoutExtension(texture.Name)) + ".dds";
            File.Copy(textureSource, textureDest, true);
        }
        
        // Copy textures from different folders
        if (Operations is not null)
        {
            foreach (OperationBase operation in Operations)
            {
                if (operation is not OperationEditMaterialTextures materials)
                {
                    continue;
                }

                CopyTexture(gameData.FullName, outputFile.Directory.FullName, materials.MainTex);
                CopyTexture(gameData.FullName, outputFile.Directory.FullName, materials.BumpMap);
                CopyTexture(gameData.FullName, outputFile.Directory.FullName, materials.Emissive);
                CopyTexture(gameData.FullName, outputFile.Directory.FullName, materials.MetalMap);
                CopyTexture(gameData.FullName, outputFile.Directory.FullName, materials.TeamColorMap);
            }
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
            return;
        }
        
        string destTex = Path.Combine(outputFolder, Path.GetFileName(texturePath)) + ".dds";

        if (!File.Exists(destTex))
        {
            File.Copy(sourceTex, destTex, true);
        }
    }

    public static ConfigModel FromYaml(string yaml)
    {
        IDeserializer deserializer = new StaticDeserializerBuilder(new YamlStaticContext())
            .WithNamingConvention(UnderscoredNamingConvention.Instance)
            .WithNodeDeserializer(new OperationBaseDeserializer())
            .Build();
        
        ConfigModel configModel = deserializer.Deserialize<ConfigModel>(yaml);

        return configModel;
    }
}