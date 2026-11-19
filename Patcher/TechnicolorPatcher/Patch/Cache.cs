using TechnicolorPatcher.Util;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace TechnicolorPatcher.Patch;

[YamlSerializable]
public class Cache
{
    public static Cache Instance
    {
        get
        {
            field ??= new Cache();
            return field;
        }
        private set;
    }

    public Dictionary<string, ModelCacheEntry> ModelEntries { get; set; } = [];
    public Dictionary<string, TextureCacheEntry> TextureEntries { get; set; } = [];

    public static void Load(string cacheFilePath)
    {
        Log.Header("Loading Cache...");
        Log.Info(new FileInfo(cacheFilePath).Name);
        
        IDeserializer serializer = new StaticDeserializerBuilder(new YamlStaticContextCustom())
            .WithNamingConvention(UnderscoredNamingConvention.Instance)
            .Build();
        
        string yaml = File.ReadAllText(cacheFilePath);
        Cache cache = serializer.Deserialize<Cache>(yaml);
        Instance = cache;
        
        Log.Info(new FileInfo(cacheFilePath).Name, MessageStatus.Ok);
    }
    
    public static void Save(string cacheFilePath)
    {
        Log.Header("Saving Cache...");
        Log.Info(new FileInfo(cacheFilePath).Name);

        ISerializer serializer = new StaticSerializerBuilder(new YamlStaticContextCustom())
            .WithNamingConvention(UnderscoredNamingConvention.Instance)
            .Build();
        
        string yaml = serializer.Serialize(Instance);
        File.WriteAllText(cacheFilePath, yaml);
        
        Log.Info(new FileInfo(cacheFilePath).Name, MessageStatus.Ok);
    }
}

[YamlSerializable]
public class ModelCacheEntry
{
    public required string InputHash { get; set; }
}

[YamlSerializable]
public class TextureCacheEntry
{
    public required string ConfigHash { get; set; }
    public required string MaskHash { get; set; }
    public required TextureCacheSubEntry[] ReferencedFiles { get; set; }
}

[YamlSerializable]
public class TextureCacheSubEntry
{
    public required string Path { get; set; }
    public required string Hash { get; set; }
}