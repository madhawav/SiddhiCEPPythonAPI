#!/usr/bin/python3
from subprocess import call
import os
from SiddhiCEP4 import SiddhiLoader

# Download extension jars
call(["mvn", "install"], cwd=os.path.dirname(os.path.abspath(__file__)) + "/Extensions")

# Add extensions
extensions_path = os.path.dirname(os.path.abspath(__file__)) + "/Extensions/jars/*"
SiddhiLoader.addExtension(extensions_path)

import unittest
import logging
from time import sleep


from SiddhiCEP4.DataTypes.LongType import LongType
from SiddhiCEP4.core.SiddhiManager import SiddhiManager
from SiddhiCEP4.core.query.output.callback.QueryCallback import QueryCallback
from SiddhiCEP4.core.util import EventPrinter
from SiddhiCEP4.core.util.EventPrinter import PrintEvent

logging.basicConfig(level=logging.INFO)


from unittest.case import TestCase

from Tests.Util.AtomicInt import AtomicInt


class TestExtensions(TestCase):
    def setUp(self):
        self.eventArrived = False
        self.count = AtomicInt(0)

    def testMathRandomFunctionWithSeed(self):
        logging.info("RandomFunctionExtension TestCase, with seed")

        # Creating SiddhiManager
        siddhiManager = SiddhiManager()

        # Creating Query
        streamDefinition = "define stream inputStream (symbol string, price long, volume long);"
        query ="@info(name = 'query1') from inputStream select symbol , math:rand(12) as randNumber " + \
            "insert into outputStream;"


        # Setting up Siddhi App
        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(streamDefinition + query)

        # Setting up callback
        _self_shaddow = self

        class ConcreteQueryCallback(QueryCallback):
            def receive(self, timestamp, inEvents, outEvents):
                PrintEvent(timestamp, inEvents, outEvents)
                _self_shaddow.count.addAndGet(len(inEvents))
                _self_shaddow.eventArrived = True
                if len(inEvents) == 3:
                    randNumbers = [0,0,0]
                    randNumbers[0] = inEvents[0].getData(1)
                    randNumbers[1] = inEvents[1].getData(1)
                    randNumbers[2] = inEvents[2].getData(1)
                    isDuplicatePresent = False

                    logging.info(randNumbers[0] + ", " + randNumbers[1])

                    if randNumbers[0] == randNumbers[1] or randNumbers[0] == randNumbers[2] or randNumbers[1] == randNumbers[2]:
                        isDuplicatePresent = True

                    _self_shaddow.assertEquals(False, isDuplicatePresent)



        siddhiAppRuntime.addCallback("query1", ConcreteQueryCallback())

        # Retrieving input handler to push events into Siddhi
        inputHandler = siddhiAppRuntime.getInputHandler("inputStream")
        # Starting event processing
        siddhiAppRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["XYZ", 60.5, LongType(200)])
        sleep(0.5)

        self.assertEqual(self.count.get(), 3)
        self.assertTrue(self.eventArrived)

        siddhiManager.shutdown()

    def testMathRandomFunctionWithoutSeed(self):
        logging.info("RandomFunctionExtension TestCase, without seed")

        # Creating SiddhiManager
        siddhiManager = SiddhiManager()

        # Creating Query
        streamDefinition = "define stream inputStream (symbol string, price long, volume long);"
        query ="@info(name = 'query1') from inputStream select symbol , math:rand() as randNumber " + \
            "insert into outputStream;"


        # Setting up Siddhi App
        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(streamDefinition + query)

        # Setting up callback
        _self_shaddow = self

        class ConcreteQueryCallback(QueryCallback):
            def receive(self, timestamp, inEvents, outEvents):
                PrintEvent(timestamp, inEvents, outEvents)
                _self_shaddow.count.addAndGet(len(inEvents))
                _self_shaddow.eventArrived = True
                if len(inEvents) == 3:
                    randNumbers = [0,0,0]
                    randNumbers[0] = inEvents[0].getData(1)
                    randNumbers[1] = inEvents[1].getData(1)
                    randNumbers[2] = inEvents[2].getData(1)
                    isDuplicatePresent = False
                    if randNumbers[0] == randNumbers[1] or randNumbers[0] == randNumbers[2] or randNumbers[1] == randNumbers[2]:
                        isDuplicatePresent = True

                    _self_shaddow.assertEquals(False, isDuplicatePresent)



        siddhiAppRuntime.addCallback("query1", ConcreteQueryCallback())

        # Retrieving input handler to push events into Siddhi
        inputHandler = siddhiAppRuntime.getInputHandler("inputStream")
        # Starting event processing
        siddhiAppRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["XYZ", 60.5, LongType(200)])
        sleep(0.1)

        self.assertEqual(self.count.get(), 3)
        self.assertTrue(self.eventArrived)

        siddhiManager.shutdown()

    def testStringRegexpFunction(self):
        logging.info("ContainsFunctionExtensionTestCase TestCase")

        # Creating SiddhiManager
        siddhiManager = SiddhiManager()

        # Creating Query
        streamDefinition = "define stream inputStream (symbol string, price long, regex string);"
        query = "@info(name = 'query1') from inputStream select symbol , " + \
                "str:regexp(symbol, regex) as beginsWithWSO2 " + \
                "insert into outputStream"


        # Setting up Siddhi App
        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(streamDefinition + query)

        # Setting up callback
        _self_shaddow = self

        class ConcreteQueryCallback(QueryCallback):
            def receive(self, timestamp, inEvents, outEvents):
                PrintEvent(timestamp, inEvents, outEvents)
                for inEvent in inEvents:
                    _self_shaddow.count.addAndGet(1)
                    if _self_shaddow.count.get() == 1:
                        _self_shaddow.assertEqual(False, inEvent.getData(1))

                    if _self_shaddow.count.get() == 2:
                        _self_shaddow.assertEqual(True, inEvent.getData(1))

                    if _self_shaddow.count.get() == 3:
                        _self_shaddow.assertEqual(False, inEvent.getData(1))

                _self_shaddow.eventArrived = True

        siddhiAppRuntime.addCallback("query1", ConcreteQueryCallback())

        # Retrieving input handler to push events into Siddhi
        inputHandler = siddhiAppRuntime.getInputHandler("inputStream")
        # Starting event processing
        siddhiAppRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["hello hi hello", 700.0, "^WSO2(.*)"])
        inputHandler.send(["WSO2 abcdh", 60.5, "WSO(.*h)"])
        inputHandler.send(["aaWSO2 hi hello", 60.5, "^WSO2(.*)"])
        sleep(0.5)

        self.assertEqual(self.count.get(), 3)
        self.assertTrue(self.eventArrived)

        siddhiManager.shutdown()

    def testStringContainsFunction(self):
        logging.info("ContainsFunctionExtensionTestCase TestCase")

        # Creating SiddhiManager
        siddhiManager = SiddhiManager()

        # Creating Query
        streamDefinition = "define stream inputStream (symbol string, price long, volume long);"
        query = "@info(name = 'query1') " + \
                 "from inputStream " + \
                 "select symbol , str:contains(symbol, 'WSO2') as isContains " + \
                 "insert into outputStream;"

        # Setting up Siddhi App
        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(streamDefinition + query)

        # Setting up callback
        _self_shaddow = self
        class ConcreteQueryCallback(QueryCallback):
            def receive(self, timestamp, inEvents, outEvents):
                PrintEvent(timestamp, inEvents, outEvents)
                for inEvent in inEvents:
                    _self_shaddow.count.addAndGet(1)
                    if _self_shaddow.count.get() == 1:
                        _self_shaddow.assertEqual(False, inEvent.getData(1))

                    if _self_shaddow.count.get() == 2:
                        _self_shaddow.assertEqual(True, inEvent.getData(1))

                    if _self_shaddow.count.get() == 3:
                        _self_shaddow.assertEqual(True, inEvent.getData(1))

                _self_shaddow.eventArrived = True


        siddhiAppRuntime.addCallback("query1", ConcreteQueryCallback())

        # Retrieving input handler to push events into Siddhi
        inputHandler = siddhiAppRuntime.getInputHandler("inputStream")
        # Starting event processing
        siddhiAppRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["One of the best middleware is from WSO2.", 60.5, LongType(200)])
        sleep(0.5)

        self.assertEqual(self.count.get(),3)
        self.assertTrue(self.eventArrived)

        siddhiManager.shutdown()


