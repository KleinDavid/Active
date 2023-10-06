using Active.App.Action;
using Active.App.Models;
using Newtonsoft.Json;
using System.Net;
using WebSocketSharp;
using Active.App.Client;
using WebSocketSharp.Server;

namespace Active;
public class Appication
{
    private WebSocketServer WebSocketServer = new();
    readonly Dictionary<string, Client> Clients = new();

    public void run()
    {
        WebSocketServer.run();
        
    }

    public void runWebsocket()
    {
        var ip = "127.0.0.1";
        var port = 4000;
        var httpsv = new HttpServer(IPAddress.Parse(ip), port);
        httpsv.AddWebSocketService<WebSocketServer>("/");
        httpsv.Start();

        Console.WriteLine("WebSocket server is listening on " + ip + ":" + port);
        Console.ReadKey(true);

        httpsv.Stop();
    }
}

class WebSocketServer : WebSocketBehavior
{
    public void run()
    {
        var ip = "127.0.0.1";
        var port = 4000;
        var httpsv = new HttpServer(IPAddress.Parse(ip), port);
        httpsv.AddWebSocketService<WebSocketServer>("/");
        httpsv.Start();

        Console.WriteLine("WebSocket server is listening on " + ip + ":" + port);
        Console.ReadKey(true);

        httpsv.Stop();
    }
    protected override void OnMessage(MessageEventArgs e)
    {
        Console.WriteLine("Received message: " + e.Data);
        dynamic data = JsonConvert.DeserializeObject(e.Data);

        var saveWebsocketClientAction = new SaveWebsocket_ClientAction().GetTransportModel();

        ServerMessage serverMessage = new();
        serverMessage.Id = data.Id;
        serverMessage.ClientActions.Add(saveWebsocketClientAction);
        Send(JsonConvert.SerializeObject(serverMessage));
    }
}