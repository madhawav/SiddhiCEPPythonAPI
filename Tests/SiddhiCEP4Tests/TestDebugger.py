import unittest
import logging
from distutils import log
from time import sleep
from unittest.case import TestCase

from SiddhiCEP4.core.SiddhiManager import SiddhiManager
from SiddhiCEP4.core.debugger.SiddhiDebugger import SiddhiDebugger
from SiddhiCEP4.core.debugger.SiddhiDebuggerCallback import SiddhiDebuggerCallback
from SiddhiCEP4.core.stream.output.StreamCallback import StreamCallback
from Tests.Util.AtomicInt import AtomicInt


class TestDebugger(TestCase):
    def setUp(self):
        self.inEventCount = AtomicInt(0)
        self.debugEventCount = AtomicInt(0)
        logging.basicConfig(level=logging.INFO)

    def getCount(self, event):
        count = 0
        while event != None:
            count += 1
            event = event.getNext()

        return count

    def test_Debugger1(self):
        logging.info("Siddi Debugger Test 1: Test next traversal in a simple query")

        siddhiManager = SiddhiManager()
        cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, volume int);"

        query = "@info(name = 'query 1') from cseEventStream select symbol, price, volume insert into OutputStream; "

        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query)

        _self_shaddow = self

        class StreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        _stream_callback = StreamCallbackImpl()
        executionPlanRuntime.addCallback("OutputStream", _stream_callback)

        inputHandler = executionPlanRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = executionPlanRuntime.debug()
        siddhiDebugger.acquireBreakPoint("query 1", SiddhiDebugger.QueryTerminal.IN)

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName,queryTerminal, debugger):
                log.info("Query: " + queryName + ":" + queryTerminal.name)
                log.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))
                if count == 1:
                    _self_shaddow.assertEquals("query 1IN", queryName + queryTerminal.name,"Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60],event.getOutputData(),"Incorrect debug event received at IN")

                elif count == 2:
                    _self_shaddow.assertEqual("query 1OUT", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60],event.getOutputData(),"Incorrect debug event received at OUT")

                elif count == 3:
                    _self_shaddow.assertEqual("query 1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),"Incorrect debug event received at IN")
                elif count == 4:
                    _self_shaddow.assertEquals("query 1OUT", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40],event.getOutputData(), "Incorrect debug event received at OUT")


                debugger.next()


        _debugger_callback = SiddhiDebuggerCallbackImpl()
        siddhiDebugger.setDebuggerCallback(_debugger_callback)

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])

        sleep(1)

        _self_shaddow.assertEquals(2, _self_shaddow.inEventCount.get(), "Invalid number of output events")
        _self_shaddow.assertEquals(4, _self_shaddow.debugEventCount.get(),"Invalid number of debug events")

        executionPlanRuntime.shutdown()
if __name__ == '__main__':
    unittest.main()