using TechnicolorPatcher.Model.Config;
using TechnicolorPatcher.Util;

namespace TechnicolorPatcher.Patch;

public static class Models
{
    public static void Patch(DirectoryInfo patcherInput, DirectoryInfo patcherOutput, DirectoryInfo gameData)
    {
        Log.Header("Processing Models...");
        
        DirectoryInfo patcherModelInput = new(Path.Combine(patcherInput.FullName, "Models"));
        DirectoryInfo patcherModelOutput = new(Path.Combine(patcherOutput.FullName, "Assets"));

        foreach (FileInfo modelConfigFile in patcherModelInput.EnumerateFiles("*.yaml", SearchOption.AllDirectories))
        {
            string modelConfigFileRelativePath = Path.GetRelativePath(patcherModelInput.FullName, modelConfigFile.FullName)[..^5];
            FileInfo destination = new(Path.Combine(patcherModelOutput.FullName, modelConfigFileRelativePath) + ".mu");
            
            string identifier = Path.Combine("Models", modelConfigFileRelativePath);
            Log.Info(identifier);

            // Skip if output would be identical to last run
            string inputHash = Hash.Sha(modelConfigFile.FullName);
            if (destination.Exists && 
                Cache.Instance.ModelEntries.TryGetValue(identifier, out ModelCacheEntry? value) &&
                value.InputHash == inputHash)
            {
                Log.Info(identifier + " (Cached)",  MessageStatus.Ok);
                continue;
            }
            
            
            try
            {
                string yaml = modelConfigFile.OpenText().ReadToEnd();

                ConfigModel configModel = ConfigModel.FromYaml(yaml);
                configModel.Apply(gameData, destination);

                // Save to Cache
                Cache.Instance.ModelEntries[identifier] = new ModelCacheEntry
                {
                    InputHash = inputHash
                };
                
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