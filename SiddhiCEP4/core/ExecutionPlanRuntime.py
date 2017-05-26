from jnius import PythonJavaClass, java_method

from SiddhiCEP4.core import siddhi_api_core_inst
from SiddhiCEP4.core.debugger.SiddhiDebugger import SiddhiDebugger
from SiddhiCEP4.core.query.output.callback.QueryCallback import QueryCallback
from SiddhiCEP4.core.stream.input.InputHandler import InputHandler
from SiddhiCEP4.core.stream.output.StreamCallback import StreamCallback


class ExecutionPlanRuntime(object):
    def __init__(self,):
        raise NotImplementedError("Initialize ExecutionPlanRuntime using Siddhi Manager")

    def __new__(cls):
        bare_instance = object.__new__(cls)
        bare_instance.execution_plan_runtime_proxy = None
        return bare_instance

    def addCallback(self, queryName, queryCallback):
        '''
        Assign callback interface to ExecutionPlanRuntime
        :param queryName:
        :param queryCallback:
        :return:
        '''
        if isinstance(queryCallback, QueryCallback):
            siddhi_api_core_inst.addExecutionPlanRuntimeQueryCallback(self.execution_plan_runtime_proxy,queryName,queryCallback._query_callback_proxy_inst)
        elif isinstance(queryCallback, StreamCallback):
            siddhi_api_core_inst.addExecutionPlanRuntimeStreamCallback(self.execution_plan_runtime_proxy, queryName,
                                                                 queryCallback._stream_callback_proxy)
        else:
            raise NotImplementedError("Unknown type of callback")
    def start(self):
        '''
        Start ExecutionPlanRuntime
        :return: void
        '''
        self.execution_plan_runtime_proxy.start()

    def shutdown(self):
        '''
        Shutdown ExecutionPlanRuntime
        :return:
        '''
        self.execution_plan_runtime_proxy.shutdown()
        del self.execution_plan_runtime_proxy

    def getInputHandler(self, streamId):
        '''
        Retrieve input handler assigned with a stream
        :param streamId: stream id of stream
        :return: InputHandler
        '''
        input_handler_proxy = self.execution_plan_runtime_proxy.getInputHandler(streamId)
        return InputHandler._fromInputHandlerProxy(input_handler_proxy)

    def debug(self):
        '''
        Retrieve the Siddhi Debugger used to debug the Execution Plan
        :return: SiddhiDebugger
        '''
        #Obtain debugger proxy class
        siddhi_debugger_proxy = self.execution_plan_runtime_proxy.debug()
        return SiddhiDebugger._fromSiddhiDebuggerProxy(siddhi_debugger_proxy)


    @classmethod
    def _fromExecutionPlanRuntimeProxy(cls, execution_plan_runtime_proxy):
        '''
        Internal Constructor to wrap around JAVA Class ExecutionPlanRuntime
        :param execution_plan_runtime_proxy:
        :return:
        '''
        instance = cls.__new__(cls)
        instance.execution_plan_runtime_proxy = execution_plan_runtime_proxy
        return instance


