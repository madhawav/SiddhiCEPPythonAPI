import SiddhiCEP3.core
from SiddhiCEP3.core import siddhi_api_core_inst
from SiddhiCEP3.core.ExecutionPlanRuntime import ExecutionPlanRuntime

class SiddhiManager(object):
    def __init__(self):
        '''
        ''Initialize a new SiddhiManager
        '''
        self._siddhi_manager_proxy =  siddhi_api_core_inst.initSiddhiManager()
    def createExecutionPlanRuntime(self,executionPlan):
        '''
        Create an Execution Plan Runtime
        :param executionPlan: SiddhiQuery (string) defining execution plan
        :return: ExecutionPlanRuntime
        '''
        execution_plan_runtime_proxy = self._siddhi_manager_proxy.createExecutionPlanRuntime(executionPlan)
        return ExecutionPlanRuntime._fromExecutionPlanRuntimeProxy(execution_plan_runtime_proxy)

    def persist(self):
        '''
        Method used persist state of current Siddhi Manager instance.
        :return: 
        '''
        self._siddhi_manager_proxy.persist()

    def restoreLastState(self):
        '''
        Method used to restore state of Current Siddhi Manager instance.
        :return: 
        '''
        self._siddhi_manager_proxy.restoreLastState()

    def shutdown(self):
        '''
        Shutdown SiddhiManager
        :return:
        '''
        self._siddhi_manager_proxy.shutdown()
        del self._siddhi_manager_proxy


