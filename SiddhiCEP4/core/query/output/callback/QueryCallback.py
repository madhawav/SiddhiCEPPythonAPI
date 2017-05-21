from multiprocessing import Lock

import SiddhiCEP4.core
from abc import ABCMeta, abstractmethod

from jnius import autoclass, java_method, PythonJavaClass


_query_callback_proxy = autoclass("org.wso2.siddhi.pythonapi.proxy.core.query.output.callback.query_callback.QueryCallbackProxy")
#_lock = Lock()

class QueryCallback(metaclass=ABCMeta):
    __metaclass__ = ABCMeta
    def __init__(self):

        self._query_callback_proxy_inst = _query_callback_proxy()
        query_callback_self = self
        class ReceiveCallback(PythonJavaClass):
            '''
            Innerclass to wrap around Java Interface
            '''
            __javainterfaces__ = ["org/wso2/siddhi/pythonapi/proxy/core/query/output/callback/query_callback/ReceiveCallbackProxy"]

            @java_method(signature='(J[Lorg/wso2/siddhi/core/event/Event;[Lorg/wso2/siddhi/core/event/Event;)V',
                         name="receive")
            def receive(self, timestamp, inEvents, outEvents):
                #_lock.acquire()
                query_callback_self.receive(timestamp,inEvents,outEvents)
                #_lock.release()
        self._query_callback_proxy_inst.setReceiveCallback(ReceiveCallback())
    @abstractmethod
    def receive(self, timestamp, inEvents, outEvents):
        pass

