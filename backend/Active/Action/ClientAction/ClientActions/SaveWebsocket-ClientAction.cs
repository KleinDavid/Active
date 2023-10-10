namespace Active.App.Act
{
    public class SaveWebsocket_ClientAction : ClientAction
    {
        public string machWas = "asfdsa";
        public SaveWebsocket_ClientAction(string id = null) : base(id) {
            TransportModelType = typeof(SaveWebsocket_ClientActionTransport);
        }
    }

    public class SaveWebsocket_ClientActionTransport : ClientAction_Transport
    { 
        public string machWas { get; set; }
    }

}
