from multiprocessing import RLock

import logging

import SiddhiCEP4.core

from abc import ABCMeta, abstractmethod

from jnius import autoclass, java_method, PythonJavaClass


_stream_callback_proxy = autoclass("org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy")

_lock = RLock()

_created_instances = [] #Hold reference to prevent python from GC callback before java does

class StreamCallback(metaclass=ABCMeta):
    '''
    StreamCallback is used to receive events from StreamJunction
    This class should be extended if one intends to get events from a Siddhi Stream.
    '''
    __metaclass__ = ABCMeta

    def __init__(self):
        self._stream_callback_proxy = _stream_callback_proxy()
        stream_callback_self = self
        class ReceiveCallback(PythonJavaClass):
            '''
            Innerclass to wrap around Java Interface
            '''
            __javainterfaces__ = ["org/wso2/siddhi/pythonapi/proxy/core/stream/output/callback/stream_callback/ReceiveCallbackProxy"]

            @java_method(signature='([Lorg/wso2/siddhi/core/event/Event;)V', name="receive")
            def receive(self, events):
                stream_callback_self.receive(events)

            @java_method(signature='()V', name="gc")
            def gc(self):
                _created_instances.remove(stream_callback_self)
                logging.trace("Java Reported GC Collected Stream Callback")

        self._receive_callback_ref = ReceiveCallback() #Hold reference to prevent python from GC callback before java does
        self._stream_callback_proxy.setReceiveCallback(self._receive_callback_ref)
        _created_instances.append(self)
    @abstractmethod
    def receive(self, events):
        pass

