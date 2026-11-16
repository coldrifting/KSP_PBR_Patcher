using TechnicolorPatcher.Util;

namespace TechnicolorPatcher.Patch;

public static class Version
{
    public static void Patch(DirectoryInfo patcherInput, DirectoryInfo patcherOutput)
    {
        Log.Header("Copying version file...");
        
        FileInfo inputVersionFile = new(Path.Combine(patcherInput.FullName, patcherInput.Name) + ".version");
        FileInfo outputVersionFile = new(Path.Combine(patcherOutput.FullName, patcherInput.Name) + ".version");

        string identifier = inputVersionFile.Name;
        Log.Info(identifier);

        try
        {
            inputVersionFile.CopyTo(outputVersionFile.FullName, true);
                
            Log.Info(identifier, MessageStatus.Ok);
        }
        catch (Exception)
        {
            Log.Info(identifier, MessageStatus.Error);

            throw;
        }
    }
}