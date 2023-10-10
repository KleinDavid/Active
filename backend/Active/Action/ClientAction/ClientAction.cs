namespace Active.App.Act
{
    public abstract class ClientAction : Action
    {
        public ClientAction(string id) : base(id) {
            TransportModelType = typeof(ClientAction_Transport);
        }

        
    }

    public class ClientAction_Transport : Action_Transport
    { 
    }
}
