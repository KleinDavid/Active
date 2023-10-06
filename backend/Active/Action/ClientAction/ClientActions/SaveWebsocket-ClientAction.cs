namespace Active.App.Action
{
    public class SaveWebsocket_ClientAction : ClientAction
    {
        public static Type TransportModelType = typeof(SaveWebsocket_ClientActionTransport);

        public SaveWebsocket_ClientAction(string id = null) : base(id)
        { 
        }
    }

    public class SaveWebsocket_ClientActionTransport : ClientAction_Transport
    {
    }

}
