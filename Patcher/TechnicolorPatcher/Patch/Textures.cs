using TechnicolorPatcher.Texture.Config;
using TechnicolorPatcher.Util;

namespace TechnicolorPatcher.Patch;

public static class Textures
{
    public static void Patch(DirectoryInfo patcherInput, DirectoryInfo patcherOutput)
    {
        Log.Header("Processing Textures...");
        
        DirectoryInfo patcherModelInput = new(Path.Combine(patcherInput.FullName, "Textures"));
        DirectoryInfo patcherModelOutput = new(Path.Combine(patcherOutput.FullName, "Assets"));

        foreach (FileInfo modelConfigFile in patcherModelInput.EnumerateFiles("*.yaml", SearchOption.AllDirectories))
        {
            FileInfo masksFile = new(modelConfigFile.FullName.Replace(".yaml", ".svg"));
            
            string modelConfigFileRelativePath = Path.GetRelativePath(patcherModelInput.FullName, modelConfigFile.FullName)[..^5];
            FileInfo destination = new(Path.Combine(patcherModelOutput.FullName, modelConfigFileRelativePath));
            
            string identifier = Path.Combine("Textures", modelConfigFileRelativePath);
            Log.Info(identifier);

            // Skip if output would be identical to last run
            // TODO - Check Cache
            
            try
            {
                string yaml = modelConfigFile.OpenText().ReadToEnd();

                ConfigTexture configTexture = ConfigTexture.FromYaml(yaml);
                configTexture.Apply(destination, masksFile);

                // Save to Cache
                // TODO - Save to Cache
                
                Log.Info(identifier, MessageStatus.Ok);
            }
            catch (Exception)
            {
                Log.Info(identifier, MessageStatus.Error);
                
                throw;
            }
        }
    }
}