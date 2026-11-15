namespace KSP_PBR_Patcher.Util;

public enum MessageStatus
{
    Info,
    Ok,
    Warning,
    Error,
}

public static class Log
{
    public static void Header(object message)
    {
        Console.ForegroundColor = ConsoleColor.DarkBlue;
        Console.WriteLine(message);
        Console.ResetColor();
    }
    
    public static void Info(object message, MessageStatus status = MessageStatus.Info)
    {
        switch (status)
        {
            case MessageStatus.Ok:
                ClearLine();
                Console.Write(" [");
                Console.ForegroundColor = ConsoleColor.DarkGreen;
                Console.Write("OK");
                Console.ResetColor();
                Console.Write("]  ");
            
                Console.ForegroundColor = ConsoleColor.Gray;
                Console.WriteLine(message);
                break;
            case MessageStatus.Warning:
                ClearLine();
                Console.Write(" [");
                Console.ForegroundColor = ConsoleColor.DarkYellow;
                Console.Write("WRN");
                Console.ResetColor();
                Console.Write("] ");
            
                Console.ForegroundColor = ConsoleColor.Gray;
                Console.WriteLine(message);
                break;
            case MessageStatus.Error:
                ClearLine();
                Console.Write(" [");
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.Write("ERR");
                Console.ResetColor();
                Console.Write("] ");
            
                Console.ForegroundColor = ConsoleColor.Gray;
                Console.WriteLine(message);
                break;
            case MessageStatus.Info:
            default:
                Console.ForegroundColor = ConsoleColor.Gray;
                Console.Write("       " + message);
                break;
        }

        Console.ResetColor();
    }

    private static void ClearLine()
    {
        Console.Write('\r');
        //Console.Write(new string(' ', Console.BufferWidth - 1));
    }
}