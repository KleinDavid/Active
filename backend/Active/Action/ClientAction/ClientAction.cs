using AutoMapper;
using Microsoft.AspNetCore.Http.HttpResults;
using System.Dynamic;
using static System.Net.Mime.MediaTypeNames;

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
