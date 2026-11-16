using System.Data;
using System.Runtime.InteropServices;

namespace TechnicolorPatcher.Util.Parser;

public static class GameData
{
    public static DirectoryInfo GetPath(DirectoryInfo? input)
    {
        DirectoryInfo? output;
        
        if (input is null)
        {
            // Check common locations
            if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                const string winDefault = @"C:\Program Files (x86)\Steam\SteamApps\common\Kerbal Space Program\GameData";
                if (Directory.Exists(winDefault))
                {
                    output = new DirectoryInfo(winDefault);
                }
                else
                {
                    const string winAlt = @"C:\Steam\SteamApps\common\Kerbal Space Program\GameData";
                    if (Directory.Exists(winAlt))
                    {
                        output = new DirectoryInfo(winAlt);
                    }
                    else
                    {
                        output = null;
                    }
                }
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
            {
                string homePath = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                
                string linuxDefault = Path.Combine(homePath, ".local/share/Steam/Steamapps/common/Kerbal Space Program/GameData");
                if (Directory.Exists(linuxDefault))
                {
                    output = new DirectoryInfo(linuxDefault);
                }
                else
                {
                    string linuxAlt = Path.Combine(homePath, ".steam/steam/steamapps/common/Kerbal Space Program/GameData");
                    if (Directory.Exists(linuxAlt))
                    {
                        output = new DirectoryInfo(linuxAlt);
                    }
                    else
                    {
                        string linuxAlt2 = Path.Combine(homePath, "Steam/steamapps/common/Kerbal Space Program/GameData");
                        if (Directory.Exists(linuxAlt2))
                        {
                            output = new DirectoryInfo(linuxAlt);
                        }
                        else
                        {
                            output = null;
                        }
                    }
                }
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
            {
                string homePath = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                string macDefault = Path.Combine(homePath, "Library/Application Support/Steam/steamapps/common/Kerbal Space Program/GameData");
                if (Directory.Exists(macDefault))
                {
                    output = new DirectoryInfo(macDefault);
                }
                else
                {
                    output = null;
                }
            }
            else
            {
                output = null;
            }
        }
        else
        {
            string path = Path.Combine(input.FullName, "GameData");
            output = Directory.Exists(path) 
                ? new DirectoryInfo(path) 
                : null;
        }

        if (output is null)
        {
            Log.Error($"ERROR: Unable to find KSP installation folder. \n" +
                      $"Use the --ksp-path command line argument to point towards a valid KSP installation folder");
            throw new DataException("Unable to find KSP installation folder");
        }
        
        if (input is null)
        {
            Log.Warn($"WARNING: No KSP directory specified. Using installation found below: \n{output}");
        }

        return output;
    }
}