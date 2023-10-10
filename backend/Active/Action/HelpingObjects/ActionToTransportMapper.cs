using AutoMapper;
using System.Reflection;

namespace Active.App.Act
{
    internal class ActionToTransportMapper
    {

        public static MethodInfo GetMethodInfo(System.Action action) => action.Method;

        public static Dictionary<string, object> GetTransportModel(Action actionInstance, Type actionType, Type transportModelType)
        {
            var method = typeof(ActionToTransportMapper).GetMethod("MapTransportModel", BindingFlags.Static | BindingFlags.NonPublic)!;

            var methodRef = method.MakeGenericMethod(actionType, transportModelType);
            var parameters = new object[] { actionInstance };
            var action = methodRef.Invoke(null, parameters)!;
            var res = new Dictionary<string, object>();
            res[actionInstance.TypeName] = action;
            return res;
        }
        private static TransportModelType MapTransportModel<ActionType, TransportModelType>(ActionType actionInstance) where TransportModelType : Action_Transport
        {
            var transport = (TransportModelType)Activator.CreateInstance(typeof(TransportModelType), new object[] { })!;
            var config = new MapperConfiguration(cfg => {
                cfg.CreateMap<ActionType, TransportModelType>();
            });

            IMapper mapper = config.CreateMapper();
            transport = mapper.Map<ActionType, TransportModelType>(actionInstance);

            return transport;
        }
    }
}
