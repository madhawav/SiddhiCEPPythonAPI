import unittest
import logging
from distutils import log
from unittest.case import TestCase

from SiddhiCEP4.core.SiddhiManager import SiddhiManager
from SiddhiCEP4.core.stream.output.StreamCallback import StreamCallback
from Tests.Util.AtomicInt import AtomicInt


class TestDebugger(TestCase):
    def setUp(self):
        self.inEventCount = AtomicInt(0)
        self.debugEventCount = AtomicInt(0)
        logging.basicConfig(level=logging.INFO)

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

        executionPlanRuntime.addCallback("OutputStream", StreamCallbackImpl())

        inputHandler = executionPlanRuntime.getInputHandler("cseEventStream")


if __name__ == '__main__':
    unittest.main()