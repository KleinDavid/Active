using Active.App.Act;

namespace Active.App.Act
{
    public class ServerAction : Action
    {
        public static Type TransportModelType = typeof(ServerAction_Transport);
        public Dictionary<string, ClientAction> outputClientActions = new();
        public ServerAction(string id) : base(id) {
            initOutputClientActions();
        }

        protected void initOutputClientActions () {}
    }

    public class ServerAction_Transport : Action_Transport
    {
        
    }
}
