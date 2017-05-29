import logging

import time

from SiddhiCEP4.core.SiddhiManager import SiddhiManager
from SiddhiCEP4.core.debugger.SiddhiDebugger import SiddhiDebugger
from SiddhiCEP4.core.debugger.SiddhiDebuggerCallback import SiddhiDebuggerCallback
from SiddhiCEP4.core.stream.output.StreamCallback import StreamCallback
from Tests.Util.AtomicInt import AtomicInt


class testen:
    def __init__(self):
        self.inEventCount = AtomicInt(0)
        self.debugEventCount = AtomicInt(0)
        logging.basicConfig(level=logging.INFO)

    def getCount(self, event):
        count = 0
        while event != None:
            count += 1
            event = event.getNext()

        return count

    def test(self):
        logging.info("Siddi Debugger Test 3: Test next traversal in a query with time batch window")

        siddhiManager = SiddhiManager()

        cseEventStream = "define stream cseEventStream (symbol string, price float, volume int);"
        query = "@info(name = 'query1')" + "from cseEventStream#window.timeBatch(3 sec) " +  "select symbol, price, volume " + "insert into OutputStream; "

        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query)

        _self_shaddow = self
        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                logging.info("Output Receive")
                _self_shaddow.inEventCount.addAndGet(len(events))

        executionPlanRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = executionPlanRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = executionPlanRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        current_milli_time = lambda: int(round(time.time() * 1000))


        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + "\t" + str(current_milli_time()))
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                # if count == 1:
                #     _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name,"Incorrect break point")
                #     _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),"Incorrect debug event received at IN")
                # elif count == 2:
                #     _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name,"Incorrect break point")
                #     _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),"Incorrect debug event received at IN")
                # elif count == 3:
                #     _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                #     _self_shaddow.assertListEqual(["WSO2", 60.0, 50],  event.getOutputData(),"Incorrect debug event received at IN")

                #next call will not reach OUT since there is a window
                logging.info("Condition End")
                debugger.next()
                logging.info("Debug End")

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])
        inputHandler.send(["WSO2", 60.0, 50])

        logging.info("Input End")
        time.sleep(4)
        logging.info("Sleep End")

        #self.assertEquals(3, self.inEventCount.get(),"Invalid number of output events")
        #self.assertEquals(3, self.debugEventCount.get(),"Invalid number of debug events")

        logging.info("Assert End")

        executionPlanRuntime.shutdown()
        siddhiManager.shutdown()

t = testen()
t.test()