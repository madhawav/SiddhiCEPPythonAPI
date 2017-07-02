#!/usr/bin/python3
import unittest
import logging
from time import sleep

from SiddhiCEP4 import DataTypes
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

    def StringContainsTestCase(self):
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
        sleep(2)

        self.assertEqual(self.count.get(),3)
        self.assertTrue(self.eventArrived)

        siddhiManager.shutdown()

    def test2(self):
        logging.info("extension test1")
        siddhiManager = SiddhiManager()

        cseEventStream = "define stream cseEventStream (symbol string, price float, volume long);"
        query = ("@info(name = 'query1') from cseEventStream select price , custom:getAll(symbol) as toConcat " + \
                    "group by volume insert into mailOutput;")
        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_copy = self
        class QueryCallbackImpl(QueryCallback):
            def receive(self, timestamp, inEvents, outEvents):
                EventPrinter.PrintEvent(timestamp, inEvents, outEvents)
                _self_copy.count = _self_copy.count + inEvents.length
                if _self_copy.count == 3:
                    _self_copy.assertEqual("WSO2ABC", inEvents[len(inEvents) - 1].getData(1))
                _self_copy.eventArrived = True

        siddhiAppRuntime.addCallback("query1",QueryCallbackImpl())

        inputHandler = siddhiAppRuntime.getInputHandler()
        siddhiAppRuntime.start()
        inputHandler.send(["IBM", 700.0, LongType.LongType(100)])
        sleep(0.1)

        inputHandler.send(["WSO2", 60.5, LongType.LongType(200)])
        sleep(0.1)

        inputHandler.send(["ABC", 60.5, LongType.LongType(200)])
        sleep(0.1)

        self.assertEqual(3, self.count)
        self.assertTrue(self.eventArrived)
        siddhiAppRuntime.shutdown()
