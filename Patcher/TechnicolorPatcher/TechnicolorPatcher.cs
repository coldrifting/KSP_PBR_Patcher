using System.CommandLine;
using System.Data;
using System.Diagnostics;
using System.Text.RegularExpressions;
using TechnicolorPatcher.Patch;
using TechnicolorPatcher.Util;
using TechnicolorPatcher.Util.Parser;
using YamlDotNet.Core;

namespace TechnicolorPatcher;

internal static partial class Program
{
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

        RootCommand rootCommand = new("Patcher to add technicolor support to various mods");
        rootCommand.Options.Add(patcherRootPathOption);
        rootCommand.Options.Add(kspPathOption);
        rootCommand.Options.Add(texconvPathOption);
        rootCommand.Options.Add(patcherSelectionOption);
        
        try
        {
            ParseResult result = rootCommand.Parse(args);
            if (result.Errors.Count > 0)
            {
                Log.Error(result.Errors);
                throw new DataException("Invalid arguments");
            }

            DirectoryInfo gameData = GameData.GetPath(result.GetValue(kspPathOption));
            DirectoryInfo patcherRoot = Root.GetPath(result.GetValue(patcherRootPathOption));
            FileInfo? texconv = Texconv.GetPath(result.GetValue(texconvPathOption));
            string? patcherSelection = result.GetValue(patcherSelectionOption);

            DirectoryInfo patcherInputRoot = new(Path.Combine(patcherRoot.FullName, "Source"));
            if (!patcherInputRoot.Exists)
            {
                Log.Warn("No patchers detected in Source folder. Exiting...");
                throw new DataException("Invalid Source folder");
            }
        
            DirectoryInfo patcherOutputRoot = new(Path.Combine(patcherRoot.FullName, "Output"));
            
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
                
                string[] matchingMods = gameData.EnumerateDirectories(modSourceName)
                    .Select(s => s.Name)
                    .ToArray();
                
                if (matchingMods.Contains(modSourceName))
                {
                    All.Patch(patcherInput, patcherOutput, gameData, texconv);
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
        Console.WriteLine("Press any key to exit...");
        Console.ReadKey();
    }

    [GeneratedRegex("PBR$")]
    private static partial Regex PbrSuffixRegex();
}