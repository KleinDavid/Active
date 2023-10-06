
using Active.App.Client;
using Tools;

namespace Active;
public class Appication
{
    private WebSocketServer WebSocketServer = new();
    readonly Dictionary<string, Client> Clients = new();

    public void run()
    {
        WebSocketServer.run();
        WebSocketServer.MessageReceived += MessageReceived; // register with an event
    }

    private void MessageReceived(object sender, EventArgs e) {
        Console.WriteLine(e);
        Console.WriteLine("david klein");
    }
}