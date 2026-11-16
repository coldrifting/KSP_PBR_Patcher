using System.Security.Cryptography;

namespace TechnicolorPatcher.Util;

public static class Hash
{
    public static string Sha(string filePath)
    {
        using FileStream stream = File.OpenRead(filePath);
        string hash = Convert.ToHexString(SHA256.Create().ComputeHash(stream));
        return hash;
    }
}