from multiprocessing import RLock

import SiddhiCEP4.core

from abc import ABCMeta, abstractmethod

from jnius import autoclass, java_method, PythonJavaClass


_stream_callback_proxy = autoclass("org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy")

_lock = RLock()
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
                _lock.acquire()
                stream_callback_self.receive(events)
                _lock.release()
        self._stream_callback_proxy.setReceiveCallback(ReceiveCallback())
    @abstractmethod
    def receive(self, events):
        pass

