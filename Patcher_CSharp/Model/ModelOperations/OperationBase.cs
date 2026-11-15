namespace KSP_PBR_Patcher.Model.ModelOperations;

public class OperationBase
{
    public virtual void Apply(MuFile muFile, string gameDataPath)
    {
        throw new NotSupportedException();
    }
}