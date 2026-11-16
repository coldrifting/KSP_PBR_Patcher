namespace TechnicolorPatcher.Model.Components.Material;

public interface IProperty
{
    public string Name { get; set; }
    
    public void Write(BinaryWriter writer);
    IProperty Clone();
}