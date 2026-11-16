using TechnicolorPatcher.Model.Components;
using TechnicolorPatcher.Model.Components.Material;
using TechnicolorPatcher.Model.Tags;
using TechnicolorPatcher.Types;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Model.Config;

[YamlSerializable]
public class ColorZone
{
    public required string Tc1 { get; set; }
    public string? Tc2 { get; set; }
    public string? Copy { get; set; }
    public List<string> Materials { get; set; } = [];
    public List<string> Transforms { get; set; } = [];

    private List<MuTransform> _outputTransforms = [];

    public static ColorZone FromYaml(Dictionary<object, object> yamlDict)
    {
        string tc1 = (string)yamlDict["tc1"];
        string? tc2 = (string?)yamlDict.GetValueOrDefault("tc2");
        string? copy = (string?)yamlDict.GetValueOrDefault("copy");
        List<string> materials = (List<string>?)yamlDict.GetValueOrDefault("materials") ?? new List<string>();
        List<string> transforms = (List<string>?)yamlDict.GetValueOrDefault("transforms") ?? new List<string>();

        return new ColorZone
        {
            Tc1 = tc1,
            Tc2 = tc2,
            Copy = copy,
            Materials = materials,
            Transforms = transforms
        };
    }
    
    public static void ApplyColorZones(MuFile muFile, Dictionary<string, ColorZone> colorZones)
    {
        HashSet<MuTag> renderableTags = [MuTag.MeshRenderer, MuTag.SkinnedMeshRenderer];
        List<MuTransform> allRenderableTransforms = muFile.GetTransforms(null, renderableTags);

        foreach (ColorZone zone in colorZones.Values)
        {
            if (zone.Transforms.Count == 0)
            {
                zone._outputTransforms.AddRange(allRenderableTransforms);
            }
            else
            {
                foreach (MuTransform transform in allRenderableTransforms)
                {
                    if (zone.Transforms.Contains(transform.Name))
                    {
                        zone._outputTransforms.Add(transform);
                    }
                }
            }

            if (zone.Materials.Count > 0)
            {
                List<int> validMaterialIndices = [];
                for (int i = 0; i < muFile.Materials.Count; i++)
                {
                    Material material = muFile.Materials[i];
                    if (zone.Materials.Contains(material.Name))
                    {
                        validMaterialIndices.Add(i);
                    }
                }

                bool[] deletions = new bool[zone._outputTransforms.Count];
                for (int i = 0; i < zone._outputTransforms.Count; i++)
                {
                    MuTransform transform = zone._outputTransforms[i];
                    if (transform.Data.ContainsKey(MuTag.MeshRenderer))
                    {
                        MuComponentRenderer renderer = (MuComponentRenderer)transform[MuTag.MeshRenderer];
                        if (!validMaterialIndices.Contains(renderer.MaterialIndex))
                        {
                            deletions[i] = true;
                        }
                    }
                    else if (transform.Data.ContainsKey(MuTag.SkinnedMeshRenderer))
                    {
                        MuComponentSkinnedMesh skinnedMesh = (MuComponentSkinnedMesh)transform[MuTag.SkinnedMeshRenderer];
                        foreach (int index in skinnedMesh.MaterialIndices)
                        {
                            if (!validMaterialIndices.Contains(index))
                            {
                                deletions[i] = true;
                            }
                        }
                    }
                    else
                    {
                        throw new ArgumentException("Shouldn't happen");
                    }
                }
                
                zone._outputTransforms = zone._outputTransforms.Where((_, index) => !deletions[index]).ToList();
            }
                
            if (zone._outputTransforms.Count == 0)
            {
                string errorMsg = "No transforms found matching the following filters: \n";
                if (zone.Transforms.Count > 0)
                {
                    errorMsg += "Transforms: \n";
                    foreach (string transform in zone.Transforms)
                    {
                        errorMsg += $"{transform} \n";
                    }
                }
                    
                if (zone.Materials.Count > 0)
                {
                    errorMsg += "Materials: \n";
                    foreach (string material in zone.Materials)
                    {
                        errorMsg += $"{material} \n";
                    }
                }

                throw new ArgumentException(errorMsg);
            }
        }
        
        // Make zones exclusive to a single transform
        List<MuTransform> usedTransforms = [];
        foreach (ColorZone zone in colorZones.Values.Reverse())
        {
            for (int i = zone._outputTransforms.Count - 1; i >= 0; i--)
            {
                if (usedTransforms.Contains(zone._outputTransforms[i]))
                {
                    zone._outputTransforms.RemoveAt(i);
                }
                else
                {
                    usedTransforms.Add(zone._outputTransforms[i]);
                }
            }
        }
        
        // Apply material changes to model
        foreach ((string zoneName, ColorZone zone) in colorZones)
        {
            (TeamColor tc1, TeamColor tc2) = TeamColorExt.GetTeamColors(zone.Tc1, zone.Tc2);
            if (zone.Copy is not null)
            {
                Material newMaterial = muFile.Materials.First(s => s.Name == zone.Copy).Clone();
                newMaterial.Name = zone.Copy + "-" + zoneName;
                muFile.Materials.Add(newMaterial);
                muFile.AssignTeamColors(newMaterial.Name, tc1, tc2);

                int newMaterialIndex = muFile.Materials.Count - 1;
                foreach (MuTransform transform in zone._outputTransforms)
                {
                    transform.SetMaterialIndex(newMaterialIndex);
                }
            }
            else
            {
                HashSet<int> materialIndicesToFix = [];
                foreach (MuTransform transform in zone._outputTransforms)
                {
                    int matIndex = transform.GetMaterialIndex();
                    materialIndicesToFix.Add(matIndex);
                }

                foreach (int materialIndex in materialIndicesToFix)
                {
                    Material material = muFile.Materials[materialIndex];
                    muFile.AssignTeamColors(material.Name, tc1, tc2);
                }
            }
        }
    }
}