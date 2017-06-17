#!/usr/bin/env python2.7

import unittest

import logging
logging.basicConfig(level=logging.INFO)

from time import sleep
from unittest.case import TestCase

from SiddhiCEP4.core.SiddhiManager import SiddhiManager
from SiddhiCEP4.core.stream.output.StreamCallback import StreamCallback
from Tests.Util.AtomicInt import AtomicInt


class TestOutputStream(TestCase):
    def setUp(self):
        self.inEventCount = AtomicInt(0)
        self.debugEventCount = AtomicInt(0)

    def getCount(self, event):
        count = 0
        while event != None:
            count += 1
            event = event.getNext()

        return count

    def test_outputstram(self):
        logging.info("OutputStream Test 1: Test reception of events")
        siddhiManager = SiddhiManager()
        cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, volume int);"

        query = "@info(name = 'query 1') from cseEventStream select symbol, price, volume insert into OutputStream; "

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class StreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", StreamCallbackImpl())

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])

        sleep(1)

        _self_shaddow.assertEqual(2, _self_shaddow.inEventCount.get(), "Invalid number of output events")


        siddhiAppRuntime.shutdown()
if __name__ == '__main__':
    unittest.main()