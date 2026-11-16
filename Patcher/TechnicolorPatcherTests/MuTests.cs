using TechnicolorPatcher.Model;
using Xunit.Abstractions;

namespace TechnicolorPatcherTests;

public class MuTests
{
    private readonly ITestOutputHelper _testOutputHelper;

    public MuTests(ITestOutputHelper testOutputHelper)
    {
        _testOutputHelper = testOutputHelper;
    }

    [Fact]
    public void TestMuFilesSaveUnchanged()
    {
        string gameDataDir = @"C:\Steam\steamapps\common\Kerbal Space Program\GameData";

        string[] modDirs =
        [
            @"Squad\Parts",
            @"SquadExpansion\Serenity\Parts",
            @"SquadExpansion\MakingHistory\Parts",
            @"ReStock\Assets",
            @"ReStockPlus\Assets",
            @"ReStockPBR\Assets",
            @"ReStockPlusPBR\Assets",
        ];

        for (int i = 0; i < modDirs.Length; i++)
        {
            modDirs[i] = Path.Combine(gameDataDir, modDirs[i]);
        }

        List<string> modelFiles = [];
        modelFiles.AddRange(modDirs.SelectMany(dir => Directory.EnumerateFiles(dir, "*.mu", SearchOption.AllDirectories)));

        foreach (string modelFile in modelFiles)
        {
            // Bugged files
            if (modelFile.EndsWith("LV-T91.mu") || modelFile.EndsWith("clydesdale-1.mu"))
            {
                continue;
            }
            
            MuFile muFile = MuFile.ReadFile(modelFile);

            byte[] input = File.ReadAllBytes(modelFile);
            byte[] versionBytes = input[4..8];
            int version = BitConverter.ToInt32(versionBytes, 0);
            if (version != 5)
            {
                _testOutputHelper.WriteLine($"Skipping version {version} model file: " + modelFile);
                continue;
            }

            _testOutputHelper.WriteLine("Testing model file: " + modelFile);

            using MemoryStream memoryStream = new();
            using BinaryWriter writer = new(memoryStream);
            muFile.Write(writer);
            writer.Flush();
            
            byte[] output = memoryStream.ToArray();

            Assert.Equal(input, output);
        }
    }
}