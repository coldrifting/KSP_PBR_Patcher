using KSP_PBR_Patcher.Util;

namespace KSP_PBR_Patcher.Patch;

public static class Assets
{
    public static void Patch(string inputModAssetPath, string outputModAssetPatch)
    {
        Log.Header("Copying pre-built models and textures...");
        string[] meshes = Directory.GetFiles(inputModAssetPath, "*.mu", SearchOption.AllDirectories);
        string[] textures = Directory.GetFiles(inputModAssetPath, "*.dds", SearchOption.AllDirectories);
        foreach (string assetFile in meshes.Concat(textures))
        {
            string outputAssetRelativePath = Path.GetRelativePath(inputModAssetPath, assetFile);
            string outputAssetFile = Path.Combine(outputModAssetPatch, outputAssetRelativePath);
            Directory.CreateDirectory(Directory.GetParent(outputAssetFile)!.FullName);

            string printName = Path.Combine("Configs", outputAssetRelativePath);
            Log.Info(printName);

            try
            {
                File.Copy(assetFile, outputAssetFile, true);
                
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