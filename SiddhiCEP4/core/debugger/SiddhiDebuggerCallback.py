from abc import ABCMeta, abstractmethod

import logging

import SiddhiCEP4.core

from jnius import autoclass, PythonJavaClass, java_method

_siddhi_debugger_callback_proxy = autoclass("org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback.SiddhiDebuggerCallbackProxy")

class SiddhiDebuggerCallback(metaclass=ABCMeta):
    __metaclass__ = ABCMeta
    def __init__(self):
        _siddhi_debugger_callback_self = self
        self._siddhi_debugger_callback_proxy_inst = _siddhi_debugger_callback_proxy()

    @abstractmethod
    def debugEvent(self, complexEvent, queryName, queryTerminal, debugger):
        pass
