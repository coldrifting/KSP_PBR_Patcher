using System.Diagnostics;
using TechnicolorPatcher.Texture;
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

                ConfigTexture configTexture = ConfigTexture.FromYaml(yaml, identifier);
                
                if (Cache.IsTextureCached(identifier, textureConfigFile, masksFile, destination))
                {
                    Log.Info(identifier + " (Cached)",  MessageStatus.Ok);
                    continue;
                }
                
                Stopwatch stopwatch = Stopwatch.StartNew();
                configTexture.Apply(destination, masksFile);

                Cache.CacheTexture(identifier, textureConfigFile, masksFile);
                
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