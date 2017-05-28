
from SiddhiCEP4.core import siddhi_api_core_inst
from enum import Enum

from jnius.reflect import autoclass

class SiddhiDebugger:

    class QueryTerminal(Enum):
        IN = autoclass("org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger.QueryTerminalProxy")().IN()
        OUT = autoclass("org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger.QueryTerminalProxy")().OUT()

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

    def acquireBreakPoint(self, queryName, queryTerminal):
        '''
        Acquire the given breakpoint
        :param queryName: name of the Siddhi query
        :param queryTerminal: queryTerminal IN or OUT endpoint of the query
        :return: 
        '''

        self.siddhi_debugger_proxy.acquireBreakPoint(queryName,queryTerminal.value)

    def setDebuggerCallback(self, siddhi_debugger_callback):
        if siddhi_debugger_callback is None:
            self.siddhi_debugger_proxy.setDebuggerCallback(None)
            return

        self.siddhi_debugger_proxy.setDebuggerCallback(siddhi_debugger_callback._siddhi_debugger_callback_proxy_inst)

    def next(self):
        '''
        Release the current lock and wait for the events arrive to the next point. For this to work, the next endpoint
        is not required to be a checkpoint marked by the user.
        For example, if user adds breakpoint only for the IN of query 1, next will track the event in OUT of query 1.
        :return: 
        '''
        self.siddhi_debugger_proxy.next()