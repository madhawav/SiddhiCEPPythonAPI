from multiprocessing import Lock

import logging

import SiddhiCEP4.core
from abc import ABCMeta, abstractmethod

from SiddhiCEP4 import SiddhiLoader
from SiddhiCEP4.core.event.Event import Event

from future.utils import with_metaclass

_query_callback_proxy = SiddhiLoader._loadType("org.wso2.siddhi.pythonapi.proxy.core.query.output.callback.query_callback.QueryCallbackProxy")
#_lock = Lock()

_created_instances = [] #Hold references to prevent python from GCing Callbacks until Java does

class QueryCallback(with_metaclass(ABCMeta,object)):
    #__metaclass__ = ABCMeta
    def __init__(self):

        self._query_callback_proxy_inst = _query_callback_proxy()
        query_callback_self = self
        class ReceiveCallback(SiddhiLoader._PythonJavaClass):
            '''
            Innerclass to wrap around Java Interface
            '''
            __javainterfaces__ = ["org/wso2/siddhi/pythonapi/proxy/core/query/output/callback/query_callback/ReceiveCallbackProxy"]

            @SiddhiLoader._java_method(signature='(J[Lorg/wso2/siddhi/core/event/Event;[Lorg/wso2/siddhi/core/event/Event;)V',
                         name="receive")
            def receive(self, timestamp, inEvents, outEvents):
                #_lock.acquire()
                if inEvents is not None:
                    inEvents = [Event._fromEventProxy(event) for event in inEvents]
                if outEvents is not None:
                    outEvents = [Event._fromEventProxy(event) for event in outEvents]
                query_callback_self.receive(timestamp,inEvents,outEvents)
                #_lock.release()

            @SiddhiLoader._java_method(signature='()V', name="gc")
            def gc(self):
                _created_instances.remove(query_callback_self)
                logging.info("Java Reported GC Collected Query Callback")
        self._receive_callback_ref = ReceiveCallback() #Hold reference to prevent python from GC callback before java does
        self._query_callback_proxy_inst.setReceiveCallback(self._receive_callback_ref)
        _created_instances.append(self)
    @abstractmethod
    def receive(self, timestamp, inEvents, outEvents):
        pass

