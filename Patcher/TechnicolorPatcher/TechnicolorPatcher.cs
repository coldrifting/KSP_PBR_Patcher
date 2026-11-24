using System.CommandLine;
using System.Data;
using System.Diagnostics;
using System.Text.RegularExpressions;
using TechnicolorPatcher.Patch;
using TechnicolorPatcher.Util;
using TechnicolorPatcher.Util.Parser;
using YamlDotNet.Core;

namespace TechnicolorPatcher;

internal static partial class Patcher
{
    public static DirectoryInfo GameDataPath
    {
        get => field ?? throw new InvalidOperationException("GameDataPath not set");
        private set;
    }

    public static DirectoryInfo? PatcherRootPath { get; private set; }
    public static FileInfo? TexConvPath { get; private set; }

    private static void Main(string[] args)
    {
        Option<DirectoryInfo?> kspPathOption = new("--ksp-path", "-k")
        {
            Description = "Path to the ksp installation to use resources from",
            DefaultValueFactory = _ => null
        };
        
        Option<DirectoryInfo?> patcherRootPathOption = new("--root-patcher-path", "-r")
        {
            Description = "Path to the patcher root folder containing the Source directory which contains patchers",
            DefaultValueFactory = _ => null
        };
        
        Option<FileInfo?> texconvPathOption = new("--texconv-path", "-t")
        {
            Description = "Path to the texconv file used for compressing textures",
            DefaultValueFactory = _ => null
        };
        
        Option<string?> patcherSelectionOption = new("--patcher", "-m")
        {
            Description = "Specify a single patcher to run",
            DefaultValueFactory = _ => null
        };
        
        Option<bool> waitOption = new("--wait", "-w")
        {
            Description = "Keep console open when errors occur",
            DefaultValueFactory = _ => true
        };

        RootCommand rootCommand = new("Patcher to add technicolor support to various mods");
        rootCommand.Options.Add(patcherRootPathOption);
        rootCommand.Options.Add(kspPathOption);
        rootCommand.Options.Add(texconvPathOption);
        rootCommand.Options.Add(patcherSelectionOption);
        rootCommand.Options.Add(waitOption);

        bool wait = true;
        try
        {
            ParseResult result = rootCommand.Parse(args);
            if (result.Errors.Count > 0)
            {
                Log.Error(result.Errors);
                throw new DataException("Invalid arguments");
            }

            GameDataPath = GameData.GetPath(result.GetValue(kspPathOption));
            PatcherRootPath = Root.GetPath(result.GetValue(patcherRootPathOption));
            TexConvPath = Texconv.GetPath(result.GetValue(texconvPathOption));
            string? patcherSelection = result.GetValue(patcherSelectionOption);
            wait = result.GetValue(waitOption);

            DirectoryInfo patcherInputRoot = new(Path.Combine(PatcherRootPath.FullName, "Source"));
            if (!patcherInputRoot.Exists)
            {
                Log.Warn("No patchers detected in Source folder. Exiting...");
                throw new DataException("Invalid Source folder");
            }
        
            DirectoryInfo patcherOutputRoot = new(Path.Combine(PatcherRootPath.FullName, "Output"));
            
            foreach (DirectoryInfo patcherInput in patcherInputRoot.GetDirectories())
            {
                if (patcherSelection is not null && patcherSelection != patcherInput.Name)
                {
                    continue;
                }

                DirectoryInfo patcherOutput = new(Path.Combine(patcherOutputRoot.FullName, patcherInput.Name));

                Regex r = PbrSuffixRegex();
                string modSourceName = patcherInput.Name == "ReStockPBR_Patch" 
                    ? "ReStockPBR" 
                    : r.Replace(patcherInput.Name, "");
                
                string[] matchingMods = GameDataPath.EnumerateDirectories(modSourceName)
                    .Select(s => s.Name)
                    .ToArray();
                
                if (matchingMods.Contains(modSourceName))
                {
                    All.Patch(patcherInput, patcherOutput);
                }
                else
                {
                    Log.Warn($"Skipping patch generation for {patcherInput.Name}:\n" +
                             $"The source mod was not found in the gamedata directory");
                }
            }
            
            Log.Header("Done!");
            Thread.Sleep(1500);
            return;
        }
        catch (YamlException e)
        {
            if (Debugger.IsAttached)
            {
                throw;
            }
            
            Log.Error($"An error occured during yaml deserialization: \n{e.Message}");
        }
        catch (Exception e)
        {
            if (Debugger.IsAttached)
            {
                throw;
            }

            Log.Error(e.GetType().Name + ": " + e.Message + "\n" + e.StackTrace);
        }

        if (wait)
        {
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }

    [GeneratedRegex("PBR$")]
    private static partial Regex PbrSuffixRegex();
}