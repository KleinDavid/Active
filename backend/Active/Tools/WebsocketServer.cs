using Active.App.Act;
using Active.App.Models;
using Newtonsoft.Json;
using System.Net;
using WebSocketSharp;
using WebSocketSharp.Server;
using NLog;

namespace Tools {
    public class WebSocketServer : WebSocketBehavior {

        protected static NLog.Logger Log = LogManager.GetLogger("");

        public event EventHandler MessageReceived; 
    public void run()
    {
        var ip = "127.0.0.1";
        var port = 4000;
        var httpsv = new HttpServer(IPAddress.Parse(ip), port);
        httpsv.AddWebSocketService<WebSocketServer>("/");
        httpsv.Start();

        Log.Debug("WebSocket server is listening on " + ip + ":" + port);
        Console.ReadKey(true);

        httpsv.Stop();
    }
    protected override void OnMessage(MessageEventArgs e)
    {
        Log.Debug("Received message: " + e.Data);
        dynamic data = JsonConvert.DeserializeObject(e.Data);

        MessageReceived?.Invoke(this, data);

        var saveWebsocketClientAction = new SaveWebsocket_ClientAction().GetTransportModel();

        ServerMessage serverMessage = new();
        serverMessage.Id = data.Id;
        serverMessage.ClientActions.Add(saveWebsocketClientAction);
        Send(JsonConvert.SerializeObject(serverMessage));
    }
}
}