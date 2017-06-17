#!/usr/bin/env python2.7

import unittest

import logging

logging.basicConfig(level=logging.INFO)

from multiprocessing import Lock
from time import sleep

from SiddhiCEP4.DataTypes.LongType import LongType
from SiddhiCEP4.core.SiddhiManager import SiddhiManager
from SiddhiCEP4.core.query.output.callback.QueryCallback import QueryCallback
from SiddhiCEP4.core.util.EventPrinter import PrintEvent


class BasicTests(unittest.TestCase):
    def setUp(self):
        # Creating SiddhiManager
        self.siddhiManager = SiddhiManager()
        self.siddhiApp = "" + "define stream cseEventStream (symbol string, price float, volume long); " + "" + "@info(name = 'query1') " + "from cseEventStream[volume < 150] " + "select symbol,price " + "insert into outputStream ;"
        # Generating runtime
        #print(self.siddhiApp)
        self.siddhiAppRuntime = self.siddhiManager.createSiddhiAppRuntime(self.siddhiApp)

    def test_input_handler(self):
        logging.info("Test1: Test Input Handler")
        # Retrieving input handler to push events into Siddhi
        inputHandler = self.siddhiAppRuntime.getInputHandler("cseEventStream")
        # Starting event processing
        self.siddhiAppRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])

    def test_siddhi_app_runtime_callback(self):
        logging.info("Test2: Test Siddhi App Runtime Callback")
        # Adding callback to retrieve output events from query

        global hitCount
        hitCount = 2

        class ConcreteQueryCallback(QueryCallback):
            def receive(self, timestamp, inEvents, outEvents):
                PrintEvent(timestamp, inEvents, outEvents)
                global hitCount
                hitCount -= 1

        self.siddhiAppRuntime.addCallback("query1", ConcreteQueryCallback())

        # Retrieving input handler to push events into Siddhi
        inputHandler = self.siddhiAppRuntime.getInputHandler("cseEventStream")
        # Starting event processing
        self.siddhiAppRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])


        sleep(0.5)
        self.assertEqual(hitCount,0)
    def tearDown(self):
        # shutting down the runtime
        self.siddhiAppRuntime.shutdown()

        # shutting down Siddhi
        self.siddhiManager.shutdown()

if __name__ == '__main__':
    unittest.main()