from time import sleep

import threading

from jnius import autoclass

event_polling_instance_manager = autoclass("org.wso2.siddhi.pythonapi.event_polling.InstanceManager")

class EventPoller:
    def __init__(self):
        self.feedbackLock = threading.RLock()
        self.pollThread = None

        self.debugCallbacks = [] #TODO: Extend with ability to detect correct callback

    def addDebugCallbackEvent(self, debug_callback_proxy):
        with self.feedbackLock:
            self.debugCallbacks.append(debug_callback_proxy)

    def initEventPolling(self):
        def pollLoop():
            event_polling_instance_manager_instance = event_polling_instance_manager()
            event_queue_instance = event_polling_instance_manager_instance.getEventQueue()
            while True:
                event = event_queue_instance.getQueuedEvent()
                if event is not None:
                    with self.feedbackLock:
                        if event.isDebuggerCallback():
                            for debug_callback in self.debugCallbacks:

                                complexEvent  = event.getComplexEvent(0)
                                queryName = event.getString(1)
                                queryTerminal = event.getQueryTerminal(2)
                                debugger = event.getSiddhiDebugger(3)



                                debug_callback.debugEvent(complexEvent, queryName, queryTerminal, debugger)
                sleep(0.05)
        self.pollThread = threading.Thread(target=pollLoop,daemon=True)
        self.pollThread.start()