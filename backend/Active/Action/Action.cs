using AutoMapper;

namespace Active.App.Action
{
    public class Action
    {
        public static Type TransportModelType = typeof(Action_Transport);
        public string Id { get; }
        public string TypeName { get; set; }
        public Action_Transport TransportModel;

        public Action(string id) {
            Id = id + Guid.NewGuid().ToString();
            TypeName = GetType().Name!;
            TransportModel = new Action_Transport();
        }

        public Dictionary<string, object> execute()
        {
            return GetTransportModel();
        }

        public Dictionary<string, object> GetTransportModel()
        {
            var method = typeof(Action).GetMethod("MapTransportModel")!;
            var methodRef = method.MakeGenericMethod(TransportModelType);
            var action = methodRef.Invoke(this, null)!;
            var res = new Dictionary<string, object>();
            res[TypeName] = action;
            return res;
        }

        protected T MapTransportModel<T>() where T : Action_Transport
        {
            var transport = (T)Activator.CreateInstance(typeof(T), new object[] {})!;
            var config = new MapperConfiguration(cfg => {
                cfg.CreateMap<Action, T>();
            });

            IMapper mapper = config.CreateMapper();
            transport = mapper.Map<Action, T> (this);

            return transport;
        }

    }

    public class Action_Transport
    {
        public string Id { get; set; }

    }
}
