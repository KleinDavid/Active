namespace Active.App.Action
{
    public class RegisterClient_ServerAction : ServerAction
    { 
        public static Type TransportModelType = typeof(RegisterClient_ServerAction_Transport);
        public Dictionary<string, ClientAction> outputClientActions = new();
        public RegisterClient_ServerAction(string id): base(id) {
            
        }

        protected void initOutputClientActions()
        {
            SaveWebsocket_ClientAction saveWebsocket = new SaveWebsocket_ClientAction(Id);
            outputClientActions.Add(saveWebsocket.Id, saveWebsocket);
        }
    }

    public class RegisterClient_ServerAction_Transport : ServerAction_Transport
    {
        string WebsocketAdress;
    }
}
