using TechnicolorPatcher.Util;

namespace TechnicolorPatcher.Patch;

public static class Assets
{
    public static void Patch(DirectoryInfo patcherInput, DirectoryInfo patcherOutput)
    {
        DirectoryInfo patcherAssetInput = new(Path.Combine(patcherInput.FullName, "Assets"));
        DirectoryInfo patcherAssetOutput = new(Path.Combine(patcherOutput.FullName, "Assets"));

        if (!patcherAssetInput.Exists)
        {
            return;
        }
        
        Log.Header("Copying pre-built models and textures...");
        
        IEnumerable<FileInfo> meshes = patcherAssetInput.EnumerateFiles("*.mu", SearchOption.AllDirectories);
        IEnumerable<FileInfo> textures = patcherAssetInput.EnumerateFiles("*.dds", SearchOption.AllDirectories);
        
        foreach (FileInfo assetFile in meshes.Concat(textures))
        {
            string assetFileRelativePath = Path.GetRelativePath(patcherAssetInput.FullName, assetFile.FullName);
            FileInfo destination = new(Path.Combine(patcherAssetOutput.FullName, assetFileRelativePath));
            
            string identifier = Path.Combine("Assets", assetFileRelativePath);
            Log.Info(identifier);

            try
            {
                Directory.CreateDirectory(destination.DirectoryName!);
                assetFile.CopyTo(destination.FullName, true);
                
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