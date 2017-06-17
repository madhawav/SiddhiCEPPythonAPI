from jnius import PythonJavaClass, java_method

from SiddhiCEP4.core import siddhi_api_core_inst
from SiddhiCEP4.core.debugger.SiddhiDebugger import SiddhiDebugger
from SiddhiCEP4.core.query.output.callback.QueryCallback import QueryCallback
from SiddhiCEP4.core.stream.input.InputHandler import InputHandler
from SiddhiCEP4.core.stream.output.StreamCallback import StreamCallback


class SiddhiAppRuntime(object):
    def __init__(self,):
        raise NotImplementedError("Initialize SiddhiAppRuntime using Siddhi Manager")

    def __new__(cls):
        bare_instance = object.__new__(cls)
        bare_instance.execution_plan_runtime_proxy = None
        return bare_instance

    def addCallback(self, queryName, queryCallback):
        '''
        Assign callback interface to SiddhiAppRuntime
        :param queryName:
        :param queryCallback:
        :return:
        '''
        if isinstance(queryCallback, QueryCallback):
            siddhi_api_core_inst.addSiddhiAppRuntimeQueryCallback(self.execution_plan_runtime_proxy,queryName,queryCallback._query_callback_proxy_inst)
        elif isinstance(queryCallback, StreamCallback):
            siddhi_api_core_inst.addSiddhiAppRuntimeStreamCallback(self.execution_plan_runtime_proxy, queryName,
                                                                 queryCallback._stream_callback_proxy)
        else:
            raise NotImplementedError("Unknown type of callback")
    def start(self):
        '''
        Start SiddhiAppRuntime
        :return: void
        '''
        self.execution_plan_runtime_proxy.start()

    def shutdown(self):
        '''
        Shutdown SiddhiAppRuntime
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
    def _fromSiddhiAppRuntimeProxy(cls, execution_plan_runtime_proxy):
        '''
        Internal Constructor to wrap around JAVA Class SiddhiAppRuntime
        :param execution_plan_runtime_proxy:
        :return:
        '''
        instance = cls.__new__(cls)
        instance.execution_plan_runtime_proxy = execution_plan_runtime_proxy
        return instance

    def getName(self):
        '''
        Returns name of ExecutionPlanContext
        :return: 
        '''
        return self.execution_plan_runtime_proxy.getName()

    #TODO: wrap Future
    def persist(self):
        '''
        Persists state
        :return: 
        '''
        return self.execution_plan_runtime_proxy.persist()

    def restoreRevision(self, revision):
        '''
        Restores revision
        :param revision: Revision
        :return: 
        '''
        self.execution_plan_runtime_proxy.restoreRevision(revision)

    def restoreLastRevision(self):
        '''
        Restores last revision
        :return: 
        '''
        self.execution_plan_runtime_proxy.restoreLastRevision()

    def snapshot(self):
        '''
        Obtains snapshot 
        :return: byteArray
        '''
        return self.execution_plan_runtime_proxy.snapshot()


