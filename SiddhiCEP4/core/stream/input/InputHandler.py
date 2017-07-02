import SiddhiCEP4.core #Initializes Runtime

from SiddhiCEP4 import SiddhiLoader
from SiddhiCEP4.DataTypes.DataWrapper import wrapData
from SiddhiCEP4.DataTypes.LongType import LongType

input_handler_proxy = SiddhiLoader.loadType("org.wso2.siddhi.pythonapi.proxy.core.stream.input.input_handler.InputHandlerProxy")
class InputHandler(object):
    def __init__(self):
        raise NotImplementedError("Initialize InputHandler using SiddhiAppRuntime")

    def __new__(cls):
        bare_instance = object.__new__(cls)
        bare_instance.input_handler_proxy = None
        return bare_instance

    def send(self,data):
        wrapped_data = wrapData(data)
        input_handler_proxy_inst = input_handler_proxy()
        input_handler_proxy_inst.send(self.input_handler_proxy, wrapped_data)

    @classmethod
    def _fromInputHandlerProxy(cls, input_handler_proxy):
        '''
        Internal Constructor to wrap around JAVA Class InputHandler
        :param input_handler_proxy:
        :return:
        '''
        instance = cls.__new__(cls)
        instance.input_handler_proxy = input_handler_proxy
        return instance
