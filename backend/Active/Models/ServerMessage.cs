namespace Active.App.Models
{
    public class ServerMessage
    {
        public string Id = "";
        public List<dynamic> ClientActions = new();
        public List<dynamic> ServerActions = new();

    }
}
