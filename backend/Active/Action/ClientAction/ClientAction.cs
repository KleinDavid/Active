namespace Active.App.Action
{
    public abstract class ClientAction : Action
    {
        public static Type TransportModelType = typeof(ClientAction_Transport);
        public ClientAction(string id) : base(id) {
        }

        
    }

    public class ClientAction_Transport : Action_Transport
    { 
    }
}
