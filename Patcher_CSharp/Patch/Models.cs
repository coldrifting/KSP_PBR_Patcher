using KSP_PBR_Patcher.Model.Config;
using KSP_PBR_Patcher.Util;

namespace KSP_PBR_Patcher.Patch;

public static class Models
{
    public static void Patch(
        string inputModModelPath, 
        string outputModAssetPath,
        string gameDataPath)
    {
        Log.Header("Processing Models...");
        IEnumerable<string> assets = Directory.EnumerateFiles(inputModModelPath, "*.yaml", SearchOption.AllDirectories);
        foreach (string asset in assets)
        {
            string assetName = Path.GetFileNameWithoutExtension(asset);
            string assetSubPath = Path.GetRelativePath(inputModModelPath ,Path.GetDirectoryName(asset)!);

            string printName = Path.Combine(assetSubPath, assetName);
            Log.Info(printName);

            try
            {
                string yaml = File.ReadAllText(asset);

                ConfigModel configModel = ConfigModel.FromYaml(yaml);
                configModel.Apply(gameDataPath, Path.Combine(outputModAssetPath, assetSubPath));

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