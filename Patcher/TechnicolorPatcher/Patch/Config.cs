using TechnicolorPatcher.Util;

namespace TechnicolorPatcher.Patch;

public static class Config
{
    public static void Patch(DirectoryInfo patcherInput, DirectoryInfo patcherOutput)
    {
        DirectoryInfo patcherConfigInput = new(Path.Combine(patcherInput.FullName, "Configs"));
        DirectoryInfo patcherConfigOutput = new(Path.Combine(patcherOutput.FullName, "Patches"));

        if (!patcherConfigInput.Exists)
        {
            return;
        }
        
        Log.Header("Copying config files...");
        
        foreach (FileInfo patchFile in patcherConfigInput.EnumerateFiles("*.cfg", SearchOption.AllDirectories))
        {
            string patchFileRelativePath = Path.GetRelativePath(patcherConfigInput.FullName, patchFile.FullName);
            FileInfo destination = new(Path.Combine(patcherConfigOutput.FullName, patchFileRelativePath));
            
            string printName = Path.Combine("Configs", patchFileRelativePath);
            Log.Info(printName);

            try
            {
                Directory.CreateDirectory(destination.DirectoryName!);
                File.Copy(patchFile.FullName, destination.FullName, true);
                
                Log.Info(printName, MessageStatus.Ok);
            }
            catch (Exception)
            {
                Log.Info(printName, MessageStatus.Error);

                throw;
            }
        }
    }
}