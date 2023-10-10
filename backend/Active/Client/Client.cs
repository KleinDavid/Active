using Active.App.Act;
using Active.App.Models;

namespace Active.App.Client
{
    public class Client
    {
        string Id { get; set; }
        public Type TypeName = typeof(Client);
        Dictionary<string, Component> Components = new();

        public Client()
        {
            Id = Guid.NewGuid().ToString();
            var registerClientServerAction = new RegisterClient_ServerAction(Id);
            registerClientServerAction.execute();
        }

        public ServerMessage executeClient()
        {
            var registerClientServerAction = new RegisterClient_ServerAction(Id);
            return new ServerMessage();
        }

        ServerMessage executeAction(string actionId, Dictionary<string, object> actionParams)
        {
            var serverMessage = new ServerMessage();
            return serverMessage;
        }
    }
}
