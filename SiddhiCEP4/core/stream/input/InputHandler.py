import SiddhiCEP4.core #Initializes Runtime
from jnius import autoclass

from SiddhiCEP4.DataTypes.LongType import LongType

input_handler_send_proxy = autoclass("org.wso2.siddhi.pythonapi.proxy.core.stream.input.input_handler.SendProxy")

class InputHandler(object):
    def __init__(self):
        raise NotImplementedError("Initialize InputHandler using ExecutionPlanRuntime")

    def __new__(cls):
        bare_instance = object.__new__(cls)
        bare_instance.input_handler_proxy = None
        return bare_instance

    def send(self,data):
        '''
        Sends data to stream
        :param data:
        :return:
        '''

        #NOTE: Directly passing list of data to org.wso2.siddhi.core.stream.input.InputHandler is not possibly since
        # Pyjnius creates the input array based on datatype of first element

        #TODO: Try to improve the logic here by reducing the number of JNI Calls

        i1 = input_handler_send_proxy(len(data))
        for d in data:
            if type(d) is float:
                i1.putFloat(d)
            elif type(d) is LongType:
                i1.putLong(int(d))
            elif type(d) is int:
                i1.putInt(d)
            elif type(d) is str:
                i1.putString(d)
            else:
                print(type(d))
        i1.send(self.input_handler_proxy)

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
