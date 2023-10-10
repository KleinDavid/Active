using Active;
using NLog;
using System.Runtime.CompilerServices;

class Program
{
    static void Main(string[] args)
    {
        startUp();
    }

    private static void startUp()
    {
        var application = new Appication();
        application.run();
    }
}
