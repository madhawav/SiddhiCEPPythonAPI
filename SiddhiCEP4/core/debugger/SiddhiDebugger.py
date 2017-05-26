from SiddhiCEP4.core import siddhi_api_core_inst
class SiddhiDebugger:
    def __init__(self):
        #TODO: Require ExecutionPlanContext to implement constructor
        raise NotImplementedError("Not Implemented")

    @classmethod
    def _fromSiddhiDebuggerProxy(cls, siddhi_debugger_proxy):
        '''
        Internal Constructor to wrap around JAVA Class SiddhiDebugger
        :param execution_plan_runtime_proxy:
        :return:
        '''
        instance = cls.__new__(cls)
        instance.siddhi_debugger_proxy = siddhi_debugger_proxy
        return instance