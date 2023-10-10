using AutoMapper;

namespace Active.App.Act
{
    public class Action
    {
        public Type TransportModelType = typeof(Action_Transport);
        public Type ActionType = typeof(Action);
        public string Id { get; }
        public string TypeName { get; set; }

        public Action(string id) {
            Id = id + "_" + Guid.NewGuid().ToString();
            ActionType = GetType();
            TypeName = GetType().Name!;
        }

        public Dictionary<string, object> execute()
        {
            return GetTransportModel();
        }

        public Dictionary<string, object> GetTransportModel()
        {
            return ActionToTransportMapper.GetTransportModel(this, ActionType, TransportModelType);
        }

    }

    public class Action_Transport
    {
        public string Id { get; set; }

    }
}
