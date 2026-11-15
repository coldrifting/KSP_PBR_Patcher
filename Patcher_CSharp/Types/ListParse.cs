namespace KSP_PBR_Patcher.Types;

public static class ListParse
{
    public static List<int> ToIntList(string input)
    {
        List<int> output = [];
        
        string[] split1 = input.Split(",");
        
        foreach (string se in split1)
        {
            if (se.Contains('-'))
            {
                string[] split2 = se.Split('-');
                int high = int.Parse(split2[1]);
                int low = int.Parse(split2[0]);
                for (int i = low; i <= high; i++)
                {
                    output.Add(i);
                }
            }
            else
            {
                output.Add(int.Parse(se));
            }
        }

        return output;
    }
}