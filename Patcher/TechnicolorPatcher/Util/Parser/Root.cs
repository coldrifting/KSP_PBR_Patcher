using System.Data;

namespace TechnicolorPatcher.Util.Parser;

public static class Root
{
    public static DirectoryInfo GetPath(DirectoryInfo? input)
    {
        if (input is { Exists: true })
        {
            return input;
        }

        DirectoryInfo currentDir = new(AppDomain.CurrentDomain.BaseDirectory);
        if (IsValidRootDirectory(currentDir))
        {
            return currentDir;
        }

        DirectoryInfo? current = currentDir;
        const int maxSearchUpDepth = 6;
        for (int i = 0; i <= maxSearchUpDepth; i++)
        {
            current = current.Parent;
            if (current is null)
            {
                break;
            }

            if (IsValidRootDirectory(current))
            {
                return current;
            }
        }
        
        Log.Error($"ERROR: Unable to find patcher source files. \n" +
                  $"Use the --root-patcher-path command line argument to point towards patcher files");
        throw new DataException("Unable to find patcher source files");
    }

    private static bool IsValidRootDirectory(DirectoryInfo directory)
    {
        DirectoryInfo sourcesDir = new(Path.Combine(directory.FullName, "Source"));
        if (sourcesDir.Exists)
        {
            DirectoryInfo[] canidatePatchFolders = sourcesDir.EnumerateDirectories().ToArray();
            if (canidatePatchFolders.Length > 0)
            {
                FileInfo[] versionFiles = canidatePatchFolders[0].EnumerateFiles("*.version").ToArray();
                if (versionFiles.Length > 0)
                {
                    return true;
                }
            }
        }

        return false;
    }
}