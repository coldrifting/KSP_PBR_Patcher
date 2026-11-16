namespace TechnicolorPatcher.Util;

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
        Console.ForegroundColor = ConsoleColor.Blue;
        Console.WriteLine(message);
        Console.ResetColor();
    }

    public static void Error(object message)
    {
        Console.ForegroundColor = ConsoleColor.Red;

        if (message is IList<object> errorList)
        {
            foreach (object error in errorList)
            {
                Console.Error.WriteLine(error);
            }
        }
        else
        {
            Console.Error.WriteLine(message);
        }
        
        Console.ResetColor();
    }

    public static void Warn(string message)
    {
        Console.ForegroundColor = ConsoleColor.Yellow;
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
                Console.ForegroundColor = ConsoleColor.Green;
                Console.Write("OK");
                Console.ResetColor();
                Console.Write("]  ");
            
                Console.ForegroundColor = ConsoleColor.Gray;

                string? messageStr = message.ToString();
                if (messageStr is not null && messageStr.EndsWith("(Cached)"))
                {
                    string messageMain = messageStr[..^7];
                    Console.Write(messageMain);
                    Console.ForegroundColor = ConsoleColor.Blue;
                    Console.Write("Cached");
                    Console.ResetColor();
                    Console.WriteLine(")");
                }
                else
                {
                    Console.WriteLine(message);
                }
                
                break;
            case MessageStatus.Warning:
                ClearLine();
                Console.Write(" [");
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.Write("WRN");
                Console.ResetColor();
                Console.Write("] ");
            
                Console.ForegroundColor = ConsoleColor.Gray;
                Console.WriteLine(message);
                break;
            case MessageStatus.Error:
                ClearLine();
                Console.Write(" [");
                Console.ForegroundColor = ConsoleColor.Red;
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