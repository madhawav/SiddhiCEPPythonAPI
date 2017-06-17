from SiddhiCEP4.core import siddhi_api_core_inst
from SiddhiCEP4.core.SiddhiAppRuntime import SiddhiAppRuntime


class SiddhiManager:
    def __init__(self):
        '''
        ''Initialize a new SiddhiManager
        '''
        self._siddhi_manager_proxy =  siddhi_api_core_inst.initSiddhiManager()
    def createSiddhiAppRuntime(self,siddhiApp):
        '''
        Create an Siddhi app Runtime
        :param siddhiApp: SiddhiQuery (string) defining siddhi app
        :return: SiddhiAppRuntime
        '''

        siddhi_app_runtime_proxy = self._siddhi_manager_proxy.createSiddhiAppRuntime(siddhiApp)
        return SiddhiAppRuntime._fromSiddhiAppRuntimeProxy(siddhi_app_runtime_proxy)

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


