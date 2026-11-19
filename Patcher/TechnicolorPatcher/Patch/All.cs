using TechnicolorPatcher.Util;

namespace TechnicolorPatcher.Patch;

public static class All
{
    public static void Patch(DirectoryInfo patcherInput, DirectoryInfo patcherOutput)
    {
        string patcherName = patcherInput.Name;
        
        Log.Header($"Generating {patcherName}...");
        
        string cacheFilePath = Path.Combine(patcherOutput.FullName, patcherName + ".cache.yaml");
        if (File.Exists(cacheFilePath))
        {
            Cache.Load(cacheFilePath);
        }

        if (!patcherOutput.Exists)
        {
            patcherOutput.Create();
        }
        
        Version.Patch(patcherInput, patcherOutput);
        Config.Patch(patcherInput, patcherOutput);
        Models.Patch(patcherInput, patcherOutput);
        Textures.Patch(patcherInput, patcherOutput);
        Assets.Patch(patcherInput, patcherOutput);

        Cache.Save(cacheFilePath);
    }
}