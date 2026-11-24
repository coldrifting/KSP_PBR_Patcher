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

    public static bool IsModelCached(string identifier, FileInfo configFile, FileInfo destination)
    {
        string inputHash = Hash.Sha(configFile.FullName);
        return destination.Exists &&
               Instance.ModelEntries.TryGetValue(identifier, out ModelCacheEntry? value) &&
               value.InputHash == inputHash;
    }

    public static void CacheModel(string identifier, FileInfo configFile)
    {
        string inputHash = Hash.Sha(configFile.FullName);
        Instance.ModelEntries[identifier] = new ModelCacheEntry
        {
            InputHash = inputHash
        };
    }

    public static bool IsTextureCached(string identifier, FileInfo configFile, FileInfo maskFile, FileInfo destination)
    { 
        string configHash = Hash.Sha(configFile.FullName);
        string maskHash = maskFile.Exists ? Hash.Sha(maskFile.FullName) : "(None)";
        FileInfo destinationAlbedo = new(destination.FullName + "-a.dds");
        FileInfo destinationMetal = new(destination.FullName + "-m.dds");
        FileInfo destinationTeamColor = new(destination.FullName + "-tc.dds");
        
        return destinationAlbedo.Exists && destinationMetal.Exists && destinationTeamColor.Exists &&
               Instance.TextureEntries.TryGetValue(identifier, out TextureCacheEntry? value) &&
               value.ConfigHash == configHash && value.MaskHash == maskHash;
    }

    public static void CacheTexture(string identifier, FileInfo configFile, FileInfo maskFile)
    {
        string configHash = Hash.Sha(configFile.FullName);
        string maskHash = maskFile.Exists ? Hash.Sha(maskFile.FullName) : "(None)";
        Instance.TextureEntries[identifier] = new TextureCacheEntry
        {
            ConfigHash = configHash,
            MaskHash = maskHash
        };
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
}