import SiddhiCEP3.core #Initializes Runtime
from jnius import autoclass

from SiddhiCEP3.DataTypes.DataWrapper import wrapData
from SiddhiCEP3.DataTypes.LongType import LongType
from SiddhiCEP4 import SiddhiLoader

input_handler_proxy = SiddhiLoader._loadType("org.wso2.siddhi.pythonapi.proxy.core.stream.input.input_handler.InputHandlerProxy")
#input_handler_send_proxy = autoclass("org.wso2.siddhi.pythonapi.proxy.core.stream.input.input_handler.SendProxy")

class InputHandler(object):
    def __init__(self):
        raise NotImplementedError("Initialize InputHandler using ExecutionPlanRuntime")

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
