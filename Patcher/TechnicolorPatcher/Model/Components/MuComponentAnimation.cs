using TechnicolorPatcher.Model.Components.Animation;
using TechnicolorPatcher.Model.IO;
using TechnicolorPatcher.Model.Tags;

namespace TechnicolorPatcher.Model.Components;

public class MuComponentAnimation : IMuComponent
{
    public required MuAnimationClip[] Clips { get; set; }
    public required string DefaultClip { get; set; }
    public bool Autoplay { get; set; }

    public static MuComponentAnimation Read(MuReader reader)
    {
        int numClips = reader.ReadInt32();
        MuAnimationClip[] clips = new MuAnimationClip[numClips];
        for (int i = 0; i < numClips; i++)
        {
            clips[i] = MuAnimationClip.Read(reader);
        }
        
        string defaultClip = reader.ReadString();
        bool autoplay = reader.ReadBoolean();

        return new MuComponentAnimation
        {
            Clips = clips,
            DefaultClip = defaultClip,
            Autoplay = autoplay
        };
    }
    
    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.Animation);

        writer.Write(Clips.Length);
        foreach (MuAnimationClip clip in Clips)
        {
            clip.Write(writer);
        }
        
        writer.Write(DefaultClip);
        writer.Write(Autoplay);
    }

    public IMuComponent Clone()
    {
        return new MuComponentAnimation
        {
            Clips = Clips.Select(c => c.Clone()).ToArray(),
            DefaultClip = DefaultClip,
            Autoplay = Autoplay
        };
    }
}