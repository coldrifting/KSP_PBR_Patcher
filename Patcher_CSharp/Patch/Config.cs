using KSP_PBR_Patcher.Util;

namespace KSP_PBR_Patcher.Patch;

public static class Config
{
    public static void Patch(string inputModPatchPath, string outputModPatchPath)
    {
        Log.Header("Copying config files...");
        foreach (string patchFile in Directory.GetFiles(inputModPatchPath, "*", SearchOption.AllDirectories))
        {
            string outputPatchRelativePath = Path.GetRelativePath(inputModPatchPath, patchFile);
            string outputPatchFile = Path.Combine(outputModPatchPath, outputPatchRelativePath);
            Directory.CreateDirectory(Directory.GetParent(outputPatchFile)!.FullName);

            string printName = Path.Combine("Configs", outputPatchRelativePath);
            Log.Info(printName);

            try
            {
                File.Copy(patchFile, outputPatchFile, true);
                
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