namespace KSP_PBR_Patcher.Model.Components;

public interface IMuComponent
{
    public void Write(BinaryWriter writer);

    public IMuComponent Clone();
}
