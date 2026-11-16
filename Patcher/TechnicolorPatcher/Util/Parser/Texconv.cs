using System.Runtime.InteropServices;

namespace TechnicolorPatcher.Util.Parser;

public static class Texconv
{
    public static FileInfo? GetPath(FileInfo? input)
    {
        if (input is not null && input.Exists)
        {
            return input;
        }

        if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
        {
            const string customPath = @"C:\Program Files\Texconv\texconv.exe";
            FileInfo fileInfo = new(customPath);
            if (fileInfo.Exists)
            {
                return fileInfo;
            }
        }
        
        string? pathValue = Environment.GetEnvironmentVariable("PATH");

        if (!string.IsNullOrEmpty(pathValue))
        {
            string[] directories = pathValue.Split(Path.PathSeparator, StringSplitOptions.RemoveEmptyEntries);
    
            foreach (string dir in directories)
            {
                DirectoryInfo? dirInfo = new DirectoryInfo(dir);
                if (dirInfo.Exists)
                {
                    string searchPattern = RuntimeInformation.IsOSPlatform(OSPlatform.Windows) ? "texconv.exe" : "texconv";
                    if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
                    {
                        foreach (FileInfo file in dirInfo.EnumerateFiles(searchPattern))
                        {
                            if (file.Exists)
                            {
                                return file;
                            }
                        }
                    }
                }
            }
        }

        Log.Warn("Texconv executable was not found on your system. \n" +
                 "To set the path manually, use the --texconv-path command line option. \n" +
                 "Texconv is required for compressing textures to DDS. \n" +
                 "You can find a version for windows here: https://github.com/microsoft/DirectXTex/releases/latest \n" +
                 "If you cannot find a version of texconv that works on your system, " +
                 "you will need to find another way to convert the output textures to DDS, or they will not look right in game.");
        
        return null;
    }
}