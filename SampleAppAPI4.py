# Creating SiddhiManager
from threading import Lock, RLock
from time import sleep

from SiddhiCEP4.DataTypes.LongType import LongType
from SiddhiCEP4.core.SiddhiManager import SiddhiManager
from SiddhiCEP4.core.debugger.SiddhiDebugger import SiddhiDebugger
from SiddhiCEP4.core.query.output.callback.QueryCallback import QueryCallback
from SiddhiCEP4.core.util.EventPrinter import PrintEvent

siddhiManager = SiddhiManager()
executionPlan = "" + "define stream cseEventStream (symbol string, price float, volume long); " + "" +"@info(name = 'query1') " +"from cseEventStream[volume < 150] " +"select symbol,price " + "insert into outputStream ;"

# Generating runtime
siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(executionPlan)
l = RLock()
l.acquire()
count = 3
l.release()

class ConcreteQueryCallback(QueryCallback):
    def receive(self, timestamp, inEvents, outEvents):
        PrintEvent(timestamp, inEvents, outEvents)
        l.acquire()
        global count
        count = count-1
        l.release()

siddhiAppRuntime.addCallback("query1",ConcreteQueryCallback())

# Retrieving input handler to push events into Siddhi
inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

# Starting event processing
siddhiAppRuntime.start()

# Sending events to Siddhi
inputHandler.send(["IBM",700.0,LongType(100)])
inputHandler.send(["WSO2", 60.5, LongType(200)])
inputHandler.send(["GOOG", 50, LongType(30)])
inputHandler.send(["IBM", 76.6, LongType(400)])
inputHandler.send(["WSO2", 45.6, LongType(50)])
sleep(5)

# shutting down the runtime
siddhiAppRuntime.shutdown()

# shutting down Siddhi
siddhiManager.shutdown()