using System.Diagnostics;
using SkiaSharp;
using TechnicolorPatcher.Texture.Config;
using TechnicolorPatcher.Texture.Layers;
using TechnicolorPatcher.Util;

namespace TechnicolorPatcher.Patch;

public static class Textures
{
    public static void Patch(DirectoryInfo patcherInput, DirectoryInfo patcherOutput)
    {
        Log.Header("Processing Textures...");
        
        DirectoryInfo patcherModelInput = new(Path.Combine(patcherInput.FullName, "Textures"));
        DirectoryInfo patcherModelOutput = new(Path.Combine(patcherOutput.FullName, "Assets"));

        foreach (FileInfo textureConfigFile in patcherModelInput.EnumerateFiles("*.yaml", SearchOption.AllDirectories))
        {
            FileInfo masksFile = new(textureConfigFile.FullName.Replace(".yaml", ".svg"));
            string textureConfigFileRelativePath = Path.GetRelativePath(patcherModelInput.FullName, textureConfigFile.FullName)[..^5];
            FileInfo destination = new(Path.Combine(patcherModelOutput.FullName, textureConfigFileRelativePath));
            
            string identifier = Path.Combine("Textures", textureConfigFileRelativePath);
            Log.Info(identifier);

            try
            {
                string yaml = textureConfigFile.OpenText().ReadToEnd();

                ConfigTexture configTexture = ConfigTexture.FromYaml(yaml);
                
                // Skip if output would be identical to last run
                string configHash = Hash.Sha(textureConfigFile.FullName);
                string maskHash = masksFile.Exists ? Hash.Sha(masksFile.FullName) : "(None)";
                FileInfo destinationAlbedo = new(Path.Combine(patcherModelOutput.FullName, textureConfigFileRelativePath) + "-a.dds");
                FileInfo destinationMetal = new(Path.Combine(patcherModelOutput.FullName, textureConfigFileRelativePath) + "-m.dds");
                FileInfo destinationTeamColor = new(Path.Combine(patcherModelOutput.FullName, textureConfigFileRelativePath) + "-tc.dds");
                if (destinationAlbedo.Exists && destinationMetal.Exists && destinationTeamColor.Exists &&
                    Cache.Instance.TextureEntries.TryGetValue(identifier, out TextureCacheEntry? value) &&
                    value.ConfigHash == configHash && value.MaskHash == maskHash)
                {
                    Log.Info(identifier + " (Cached)",  MessageStatus.Ok);
                    continue;
                }
                
                Stopwatch stopwatch = Stopwatch.StartNew();
                configTexture.Apply(destination, masksFile);

                // Save to Cache
                Cache.Instance.TextureEntries[identifier] = new TextureCacheEntry
                {
                    ConfigHash = configHash,
                    MaskHash = maskHash
                };
                
                stopwatch.Stop();
                Log.Info(identifier + " (" + stopwatch.ElapsedMilliseconds + "ms)", MessageStatus.Ok);
            }
            catch (Exception)
            {
                Log.Info(identifier, MessageStatus.Error);
                
                throw;
            }
        }
    }
}