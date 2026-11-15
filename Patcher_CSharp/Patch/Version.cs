using KSP_PBR_Patcher.Util;

namespace KSP_PBR_Patcher.Patch;

public static class Version
{
    public static void Patch(string inputModRootPath, string outputModRootPath)
    {
        Log.Header("Copying version file...");
        
        string modName = Path.GetFileNameWithoutExtension(inputModRootPath);

        string inputVersionFile = Path.Combine(inputModRootPath, modName) + ".version";
        string outputVersionFile = Path.Combine(outputModRootPath, modName) + ".version";

        Console.WriteLine(Path.GetFileName(inputVersionFile));
        File.Copy(inputVersionFile, outputVersionFile, true);
    }
}