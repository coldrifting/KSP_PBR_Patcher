using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Model.Operations;

[YamlSerializable]
public class OperationBase
{
    public virtual void Apply(MuFile muFile, string gameDataPath)
    {
        throw new NotSupportedException();
    }
}