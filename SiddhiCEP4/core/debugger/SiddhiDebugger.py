
from SiddhiCEP4.DataTypes.DataWrapper import unwrapHashMap
from SiddhiCEP4.core import siddhi_api_core_inst
from enum import Enum

from jnius.reflect import autoclass

from SiddhiCEP4.core import event_polling_instance

class SiddhiDebugger:

    class QueryTerminal(Enum):
        IN = autoclass("org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger.QueryTerminalProxy")().IN()
        OUT = autoclass("org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger.QueryTerminalProxy")().OUT()

        @classmethod
        def _map_value(cls, queryTerminalProxy):
            qt_value = None
            if queryTerminalProxy.isValueOut():
                qt_value = SiddhiDebugger.QueryTerminal.OUT
            elif queryTerminalProxy.isValueIn():
                qt_value = SiddhiDebugger.QueryTerminal.IN
            else:
                raise TypeError("Unknown QueryTerminal Value")
            return SiddhiDebugger.QueryTerminal(qt_value)

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

    def releaseBreakPoint(self, queryName, queryTerminal):
        '''
        Release the given breakpoint from the SiddhiDebugger.
        :param queryName: name of the Siddhi query
        :param queryTerminal: IN or OUT endpoint of the query
        :return: 
        '''
        self.siddhi_debugger_proxy.releaseBreakPoint(queryName, queryTerminal.value)

    def checkBreakPoint(self, queryName, queryTerminal, complexEvent):
        '''
        Check for active breakpoint at the given endpoint and if there is an active checkpoint, block the thread and 
        send the event for debug callback. 
        
        :param queryName: name of the Siddhi query 
        :param queryTerminal: IN or OUT endpoint of the query 
        :param complexEvent the complexEvent which is waiting at the endpoint
        :return: 
        '''
        self.siddhi_debugger_proxy.checkBreakPoint(queryName,queryTerminal.value,complexEvent._complex_event_proxy)

    def releaseAllBreakPoints(self):
        '''
        Release all the breakpoints from the Siddhi debugger. This may required to before stopping the debugger.
        :return: 
        '''
        self.siddhi_debugger_proxy.releaseAllBreakPoints()



    def getQueryState(self, queryName):
        '''
        Get all the events stored in the snapshotable entities of the given query
        :param queryName: name of the siddhi query
        :return: QueryState internal state of the query
        '''
        return unwrapHashMap(self.siddhi_debugger_proxy.getQueryState(queryName))

    def acquireBreakPoint(self, queryName, queryTerminal):
        '''
        Acquire the given breakpoint
        :param queryName: name of the Siddhi query
        :param queryTerminal: queryTerminal IN or OUT endpoint of the query
        :return: 
        '''

        self.siddhi_debugger_proxy.acquireBreakPoint(queryName,queryTerminal.value)

    def setDebuggerCallback(self, siddhi_debugger_callback):
        #if siddhi_debugger_callback is None:
        #    self.siddhi_debugger_proxy.setDebuggerCallback(None)
        #    return

        self.siddhi_debugger_proxy.setDebuggerCallback(siddhi_debugger_callback._siddhi_debugger_callback_proxy_inst)

        event_polling_instance.addDebugCallbackEvent(siddhi_debugger_callback)

    def play(self):
        '''
        Release the current lock and wait for the next event arrive to the same break point.
        :return: 
        '''
        self.siddhi_debugger_proxy.play()

    def next(self):
        '''
        Release the current lock and wait for the events arrive to the next point. For this to work, the next endpoint
        is not required to be a checkpoint marked by the user.
        For example, if user adds breakpoint only for the IN of query 1, next will track the event in OUT of query 1.
        :return: 
        '''
        self.siddhi_debugger_proxy.next()