using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;

namespace TechnicolorPatcher.Model.Components.Material;

public static class LegacyMaterialLookup
{
    public static string GetShaderName(LegacyMaterialTag matType)
    {
        return matType switch
        {
            LegacyMaterialTag.Custom =>                 "",
            LegacyMaterialTag.Diffuse =>                "KSP/Diffuse",
            LegacyMaterialTag.Specular =>               "KSP/Specular",
            LegacyMaterialTag.Bumped =>                 "KSP/Bumped",
            LegacyMaterialTag.BumpedSpecular =>         "KSP/Bumped Specular",
            LegacyMaterialTag.Emissive =>               "KSP/Emissive",
            LegacyMaterialTag.EmissiveSpecular =>       "KSP/Emissive/Specular",
            LegacyMaterialTag.EmissiveBumpedSpecular => "KSP/Emissive/Bumped Specular",
            LegacyMaterialTag.AlphaCutoff =>            "KSP/Alpha/Cutoff",
            LegacyMaterialTag.AlphaCutoffBumped =>      "KSP/Alpha/Cutoff Bumped",
            LegacyMaterialTag.Alpha =>                  "KSP/Alpha/Translucent",
            LegacyMaterialTag.AlphaSpecular =>          "KSP/Alpha/Translucent Specular",
            LegacyMaterialTag.AlphaUnlit =>             "KSP/Alpha/Unlit Transparent",
            LegacyMaterialTag.Unlit =>                  "KSP/Unlit",
            LegacyMaterialTag.ParticlesAlphaBlended =>  "KSP/Particles/Alpha Blended",
            LegacyMaterialTag.ParticlesAdditive =>      "KSP/Particles/Additive",
            _ => throw new ArgumentException("Unknown Tag Type")
        };
    }
    
    public static IProperty[] GetProperties(LegacyMaterialTag matType, MuReader reader)
    {
        switch (matType)
        {
            case LegacyMaterialTag.Diffuse:
                PropertyTexture mainTexDiffuse = PropertyTexture.Read(reader, "_MainTex");
                return [mainTexDiffuse];
            
            case LegacyMaterialTag.Specular:
                PropertyTexture mainTexSpecular = PropertyTexture.Read(reader, "_MainTex");
                PropertyColor specColorSpecular = PropertyColor.Read(reader, "_SpecColor");
                PropertyFloat3 shininessSpecular = PropertyFloat3.Read(reader, "_Shininess");
                return [mainTexSpecular, specColorSpecular, shininessSpecular];
            
            case LegacyMaterialTag.Bumped:
                PropertyTexture mainTexBumped = PropertyTexture.Read(reader, "_MainTex");
                PropertyTexture bumpMapBumped = PropertyTexture.Read(reader, "_BumpMap");
                return [mainTexBumped, bumpMapBumped];

            case LegacyMaterialTag.BumpedSpecular:
                PropertyTexture mainTexBumpedSpecular = PropertyTexture.Read(reader, "_MainTex");
                PropertyTexture bumpMapBumpedSpecular = PropertyTexture.Read(reader, "_BumpMap");
                PropertyColor specColorBumpedSpecular = PropertyColor.Read(reader, "_SpecColor");
                PropertyFloat3 shininessBumpedSpecular = PropertyFloat3.Read(reader, "_Shininess");
                return [mainTexBumpedSpecular, bumpMapBumpedSpecular, specColorBumpedSpecular, shininessBumpedSpecular];

            case LegacyMaterialTag.Emissive:
                PropertyTexture mainTexEmissive = PropertyTexture.Read(reader, "_MainTex");
                PropertyTexture emissiveEmissive = PropertyTexture.Read(reader, "_Emissive");
                PropertyColor emissiveColorEmissive = PropertyColor.Read(reader, "_EmissiveColor");
                return [mainTexEmissive, emissiveEmissive, emissiveColorEmissive];

            case LegacyMaterialTag.EmissiveSpecular:
                PropertyTexture mainTexEmissiveSpecular = PropertyTexture.Read(reader, "_MainTex");
                PropertyColor specColorEmissiveSpecular = PropertyColor.Read(reader, "_SpecColor");
                PropertyFloat3 shininessEmissiveSpecular = PropertyFloat3.Read(reader, "_Shininess");
                PropertyTexture emissiveEmissiveSpecular = PropertyTexture.Read(reader, "_Emissive");
                PropertyColor emissiveColorEmissiveSpecular = PropertyColor.Read(reader, "_EmissiveColor");
                return
                [
                    mainTexEmissiveSpecular,
                    specColorEmissiveSpecular,
                    shininessEmissiveSpecular,
                    emissiveEmissiveSpecular,
                    emissiveColorEmissiveSpecular
                ];

            case LegacyMaterialTag.EmissiveBumpedSpecular:
                PropertyTexture mainTexEmissiveBumpedSpecular = PropertyTexture.Read(reader, "_MainTex");
                PropertyTexture bumpMapEmissiveBumpedSpecular = PropertyTexture.Read(reader, "_BumpMap");
                PropertyColor specColorEmissiveBumpedSpecular = PropertyColor.Read(reader, "_SpecColor");
                PropertyFloat3 shininessEmissiveBumpedSpecular = PropertyFloat3.Read(reader, "_Shininess");
                PropertyTexture emissiveEmissiveBumpedSpecular = PropertyTexture.Read(reader, "_Emissive");
                PropertyColor emissiveColorEmissiveBumpedSpecular = PropertyColor.Read(reader, "_EmissiveColor");
                return
                [
                    mainTexEmissiveBumpedSpecular,
                    bumpMapEmissiveBumpedSpecular,
                    specColorEmissiveBumpedSpecular,
                    shininessEmissiveBumpedSpecular,
                    emissiveEmissiveBumpedSpecular,
                    emissiveColorEmissiveBumpedSpecular
                ];

            case LegacyMaterialTag.AlphaCutoff:
                PropertyTexture mainTexAlphaCutoff = PropertyTexture.Read(reader, "_MainTex");
                PropertyFloat3 cutoffAlphaCutoff = PropertyFloat3.Read(reader, "_Cutoff");
                return [mainTexAlphaCutoff, cutoffAlphaCutoff];

            case LegacyMaterialTag.AlphaCutoffBumped:
                PropertyTexture mainTexAlphaCutoffBumped = PropertyTexture.Read(reader, "_MainTex");
                PropertyTexture bumpMapAlphaCutoffBumped = PropertyTexture.Read(reader, "_BumpMap");
                PropertyFloat3 cutoffAlphaCutoffBumped = PropertyFloat3.Read(reader, "_Cutoff");
                return [mainTexAlphaCutoffBumped, bumpMapAlphaCutoffBumped, cutoffAlphaCutoffBumped];

            case LegacyMaterialTag.Alpha:
                PropertyTexture mainTexAlpha = PropertyTexture.Read(reader, "_MainTex");
                return [mainTexAlpha];

            case LegacyMaterialTag.AlphaSpecular:
                PropertyTexture mainTexAlphaSpecular = PropertyTexture.Read(reader, "_MainTex");
                PropertyFloat3 glossAlphaSpecular = PropertyFloat3.Read(reader, "_Gloss");
                PropertyColor specColorAlphaSpecular = PropertyColor.Read(reader, "_SpecColor");
                PropertyFloat3 shininessAlphaSpecular = PropertyFloat3.Read(reader, "_Shininess");
                return [mainTexAlphaSpecular, glossAlphaSpecular, specColorAlphaSpecular, shininessAlphaSpecular];

            case LegacyMaterialTag.AlphaUnlit:
                PropertyTexture mainTexAlphaUnlit = PropertyTexture.Read(reader, "_MainTex");
                PropertyColor colorAlphaUnlit = PropertyColor.Read(reader, "_Color");
                return [mainTexAlphaUnlit, colorAlphaUnlit];

            case LegacyMaterialTag.Unlit:
                PropertyTexture mainTexUnlit = PropertyTexture.Read(reader, "_MainTex");
                PropertyColor colorUnlit = PropertyColor.Read(reader, "_Color");
                return [mainTexUnlit, colorUnlit];

            case LegacyMaterialTag.ParticlesAlphaBlended:
                PropertyTexture mainTexParticlesAlphaBlended = PropertyTexture.Read(reader, "_MainTex");
                PropertyColor colorParticlesAlphaBlended = PropertyColor.Read(reader, "_Color");
                PropertyFloat3 invFadeParticlesAlphaBlended = PropertyFloat3.Read(reader, "_InvFade");
                return [mainTexParticlesAlphaBlended, colorParticlesAlphaBlended, invFadeParticlesAlphaBlended];

            case LegacyMaterialTag.ParticlesAdditive:
                PropertyTexture mainTexParticlesAdditive = PropertyTexture.Read(reader, "_MainTex");
                PropertyColor colorParticlesAdditive = PropertyColor.Read(reader, "_Color");
                PropertyFloat3 invFadeParticlesAdditive = PropertyFloat3.Read(reader, "_InvFade");
                return [mainTexParticlesAdditive, colorParticlesAdditive, invFadeParticlesAdditive];

            case LegacyMaterialTag.Custom:
            default:
                throw new ArgumentException("Unknown material tag");
        }
        
    }
}