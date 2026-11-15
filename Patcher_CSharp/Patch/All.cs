using KSP_PBR_Patcher.Util;
using YamlDotNet.Core;

namespace KSP_PBR_Patcher.Patch;

public static class All
{
    public static void Patch(string rootPath, string gameDataPath, string texconvPath, string modName)
    {
        try
        {
            string inputRootPath = Path.Combine(rootPath, "Source");
            string inputModRootPath = Path.Combine(inputRootPath, modName);
            string inputModAssetPath = Path.Combine(inputModRootPath, "Assets");
            string inputModPatchPath = Path.Combine(inputModRootPath, "Configs");
            string inputModTexturePath = Path.Combine(inputModRootPath, "Textures");
            string inputModModelPath = Path.Combine(inputModRootPath, "Models");
                
            string outputRootPath = Path.Combine(rootPath, "Output");
            string outputModRootPath = Path.Combine(outputRootPath, modName);
            string outputModAssetPath = Path.Combine(outputModRootPath, "Assets");
            string outputModPatchPath = Path.Combine(outputModRootPath, "Patches");

            Log.Header($"Generating {modName}...");
            
            Version.Patch(inputModRootPath, outputModRootPath);
            Config.Patch(inputModPatchPath, outputModPatchPath);
            Models.Patch(inputModModelPath, outputModAssetPath, gameDataPath);
            Assets.Patch(inputModAssetPath, outputModAssetPath);
        }
        catch(YamlException e)
        {
            Console.Error.WriteLine("An error occured during yaml deserialization");
            Console.Error.WriteLine(e.Message);
        }
    }
}