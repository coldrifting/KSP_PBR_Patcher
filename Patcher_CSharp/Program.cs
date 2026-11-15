using System.Diagnostics;
using KSP_PBR_Patcher.Patch;

namespace KSP_PBR_Patcher;

class Program
{
    static void Main(string[] args)
    {
        // TODO - Don't hardcode this
        const string rootPath = @"C:\Users\coldrifting\Documents\Games\KSP\Source\KSP_PBR_Patcher";
        const string gameDataPath = @"C:\Steam\Steamapps\common\Kerbal Space Program\GameData";
        const string texconvPath = @"C:\Program Files\texconv\texconv.exe";

        try
        {
            string patchDataPath = Path.Combine(rootPath, "Source");
            foreach (string patchModPath in Directory.GetDirectories(patchDataPath))
            {
                string modName = Path.GetFileName(patchModPath);

                // TODO - Temp placeholder
                if (modName == "NearFutureLaunchVehiclesPBR")
                {
                    All.Patch(rootPath, gameDataPath, texconvPath, modName);
                }
            }
        }
        catch (Exception e)
        {
            if (Debugger.IsAttached)
            {
                throw;
            }

            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine(e.GetType().Name + " : " + e.Message);
            Console.WriteLine(e.StackTrace);
            Console.ResetColor();
        }
    }
}