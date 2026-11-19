using System.Text.RegularExpressions;

namespace TechnicolorPatcher.Util;

public static partial class CaseConverter
{
    public static string ToSnakeCase(string input)
    {
        return MyRegex().Replace(input, "_$&");
    }

    [GeneratedRegex("[A-Z]")]
    private static partial Regex MyRegex();
}