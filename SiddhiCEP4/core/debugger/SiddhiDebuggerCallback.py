from abc import ABCMeta, abstractmethod

import logging

import SiddhiCEP4.core

from jnius import autoclass, PythonJavaClass, java_method


#_lock = Lock()
from SiddhiCEP4.core.debugger.SiddhiDebugger import SiddhiDebugger

_siddhi_debugger_callback_proxy = autoclass("org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback.SiddhiDebuggerCallbackProxy")

_created_instances = [] #Hold reference to prevent python from GC callback before java does

class SiddhiDebuggerCallback(metaclass=ABCMeta):
    __metaclass__ = ABCMeta
    def __init__(self):
        _siddhi_debugger_callback_self = self
        self._siddhi_debugger_callback_proxy_inst = _siddhi_debugger_callback_proxy()
        class SiddhiDebuggerCallbackProxy(PythonJavaClass):
            '''
            Innerclass to wrap around Java Interface
            '''
            __javainterfaces__ = ["org/wso2/siddhi/pythonapi/proxy/core/debugger/siddhi_debugger_callback/DebugEventCallbackProxy"]

            @java_method(signature='(Lorg/wso2/siddhi/core/event/ComplexEvent;Ljava/lang/String;Lorg/wso2/siddhi/pythonapi/proxy/core/debugger/siddhi_debugger/QueryTerminalProxy;Lorg/wso2/siddhi/core/debugger/SiddhiDebugger;)V',
                         name="debugEvent")
            def debugEvent(self, complexEvent, queryName, queryTerminal, debugger):
                #_lock.acquire()
                qt_value = None
                if queryTerminal.isValueOut():
                    qt_value = SiddhiDebugger.QueryTerminal.OUT
                elif queryTerminal.isValueIn():
                    qt_value = SiddhiDebugger.QueryTerminal.IN
                else:
                    raise TypeError("Unknown QueryTerminal Value")

                _siddhi_debugger_callback_self.debugEvent(complexEvent, queryName, SiddhiDebugger.QueryTerminal(qt_value), SiddhiDebugger._fromSiddhiDebuggerProxy(debugger))
                #_lock.release()

            @java_method(signature='()V', name="gc")
            def gc(self):
                _created_instances.remove(_siddhi_debugger_callback_self)
                logging.info("Java Reported Siddhi Debugger Callback GC")

        self._siddhi_debugger_callback_proxy_ref = SiddhiDebuggerCallbackProxy() #Hold reference to prevent python from GC callback before java does
        self._siddhi_debugger_callback_proxy_inst.setDebugEventCallback(self._siddhi_debugger_callback_proxy_ref)
        _created_instances.append(self) #Hold reference to prevent python from GC callback before java does
    @abstractmethod
    def debugEvent(self, complexEvent, queryName, queryTerminal, debugger):
        pass
