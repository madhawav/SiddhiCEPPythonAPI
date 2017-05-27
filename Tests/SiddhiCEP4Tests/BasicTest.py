import unittest
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
        self.executionPlan = "" + "define stream cseEventStream (symbol string, price float, volume long); " + "" + "@info(name = 'query1') " + "from cseEventStream[volume < 150] " + "select symbol,price " + "insert into outputStream ;"
        # Generating runtime
        self.executionPlanRuntime = self.siddhiManager.createExecutionPlanRuntime(self.executionPlan)

    def test_input_handler(self):
        # Retrieving input handler to push events into Siddhi
        inputHandler = self.executionPlanRuntime.getInputHandler("cseEventStream")
        # Starting event processing
        self.executionPlanRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])
        inputHandler.send(["WSO2", 45.6, LongType(50)])
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])
        inputHandler.send(["WSO2", 45.6, LongType(50)])
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])
        inputHandler.send(["WSO2", 45.6, LongType(50)])
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])
        inputHandler.send(["WSO2", 45.6, LongType(50)])

    def test_execution_plan_runtime_callback(self):
        # Adding callback to retrieve output events from query
        lock = Lock()

        global hitCount
        hitCount = 18

        class ConcreteQueryCallback(QueryCallback):
            def receive(self, timestamp, inEvents, outEvents):
                PrintEvent(timestamp, inEvents, outEvents)
                global hitCount
                hitCount -= 1

        _concrete_query_callback = ConcreteQueryCallback()
        self.executionPlanRuntime.addCallback("query1", _concrete_query_callback)

        # Retrieving input handler to push events into Siddhi
        inputHandler = self.executionPlanRuntime.getInputHandler("cseEventStream")
        # Starting event processing
        self.executionPlanRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])
        inputHandler.send(["WSO2", 45.6, LongType(50)])
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])
        inputHandler.send(["WSO2", 45.6, LongType(50)])
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])
        inputHandler.send(["WSO2", 45.6, LongType(50)])
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])
        inputHandler.send(["WSO2", 45.6, LongType(50)])
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])
        inputHandler.send(["WSO2", 45.6, LongType(50)])
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])
        inputHandler.send(["WSO2", 45.6, LongType(50)])

        sleep(0.5)
        self.assertEqual(hitCount,0)
    def tearDown(self):
        # shutting down the runtime
        self.executionPlanRuntime.shutdown()

        # shutting down Siddhi
        self.siddhiManager.shutdown()

if __name__ == '__main__':
    unittest.main()