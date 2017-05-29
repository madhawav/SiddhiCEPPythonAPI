import unittest
import logging
from datetime import datetime
import time
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


        executionPlanRuntime.addCallback("OutputStream", StreamCallbackImpl()) #Causes GC Error

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


        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])

        sleep(0.1)

        self.assertEquals(2, _self_shaddow.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(4, _self_shaddow.debugEventCount.get(),"Invalid number of debug events")

        executionPlanRuntime.shutdown()
        siddhiManager.shutdown()


    def test_debugger2(self):
        logging.info("Siddi Debugger Test 2: Test next traversal in a query with length batch window")

        siddhiManager = SiddhiManager()

        cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, volume int);"
        query = "@info(name = 'query1') from cseEventStream#window.lengthBatch(3) select symbol, price, volume insert into OutputStream; "

        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query)

        _self_shaddow = self
        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        executionPlanRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = executionPlanRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = executionPlanRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                log.info("Query: " + queryName + ":" + queryTerminal.name)
                log.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if count == 1:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name,"Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),"Incorrect debug event received at IN")
                elif count == 2:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name,"Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40],event.getOutputData(),"Incorrect debug event received at IN")
                elif count == 3:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 60.0, 50],  event.getOutputData(),"Incorrect debug event received at IN")
                elif count == 4:
                    _self_shaddow.assertEquals("query1OUT", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertEquals(3, _self_shaddow.getCount(event),"Incorrect number of events received")

                debugger.next()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])
        inputHandler.send(["WSO2", 60.0, 50])

        sleep(0.1)

        self.assertEquals(3, self.inEventCount.get(),"Invalid number of output events")
        self.assertEquals(6, self.debugEventCount.get(),"Invalid number of debug events")

        executionPlanRuntime.shutdown()
        siddhiManager.shutdown()


    def test_debugger3(self):
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

                if count == 1:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name,"Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),"Incorrect debug event received at IN")
                elif count == 2:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name,"Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),"Incorrect debug event received at IN")
                elif count == 3:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 60.0, 50],  event.getOutputData(),"Incorrect debug event received at IN")

                #next call will not reach OUT since there is a window
                debugger.next()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])
        inputHandler.send(["WSO2", 60.0, 50])

        sleep(4)

        self.assertEquals(3, self.inEventCount.get(),"Invalid number of output events")
        self.assertEquals(3, self.debugEventCount.get(),"Invalid number of debug events")


        executionPlanRuntime.shutdown()
        siddhiManager.shutdown()


    def test_debugger4(self):
        logging.info("Siddi Debugger Test 4: Test next traversal in a query with time batch window where next call delays 1 sec")

        siddhiManager = SiddhiManager()

        cseEventStream = "define stream cseEventStream (symbol string, price float, volume int);"
        query = "@info(name = 'query1')" + \
                "from cseEventStream#window.timeBatch(1 sec) " + \
                "select symbol, price, volume " + \
                "insert into OutputStream; "

        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query)

        _self_shaddow = self
        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))
                _self_shaddow.assertEquals(1, events.length,"Cannot emit all three in one time")

        executionPlanRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = executionPlanRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = executionPlanRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)



        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if count != 1 and queryTerminal.name == SiddhiDebugger.QueryTerminal.IN.name:
                    sleep(1.1)

                #next call will not reach OUT since there is a window
                debugger.next()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])
        inputHandler.send(["WSO2", 60.0, 50])

        sleep(1.5)

        self.assertEquals(3, self.inEventCount.get(),"Invalid number of output events")
        self.assertEquals(3, self.debugEventCount.get(),"Invalid number of debug events")


        executionPlanRuntime.shutdown()
        siddhiManager.shutdown()


    def test_debugger5(self):
        logging.info("Siddi Debugger Test 5: Test play in a simple query")

        siddhiManager = SiddhiManager()

        cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, " + \
                "volume int);"
        query = "@info(name = 'query1')" + \
                "from cseEventStream " + \
                "select symbol, price, volume " + \
                "insert into OutputStream; "

        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query)

        _self_shaddow = self
        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        executionPlanRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = executionPlanRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = executionPlanRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)


        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                log.info("Query: " + queryName + ":" + queryTerminal.name)
                log.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if count == 1:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),"Incorrect debug event received at IN")
                elif count == 2:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),"Incorrect debug event received at OUT")


                debugger.play()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])

        sleep(0.1)

        self.assertEquals(2, self.inEventCount.get(),"Invalid number of output events")
        self.assertEquals(2, self.debugEventCount.get(),"Invalid number of debug events")


        executionPlanRuntime.shutdown()
        siddhiManager.shutdown()

    def test_debugger6(self):
        logging.info("Siddi Debugger Test 6: Test play traversal in a query with length batch window")

        siddhiManager = SiddhiManager()

        cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, " + \
                "volume int);"
        query =  "@info(name = 'query1')" + \
                "from cseEventStream#window.lengthBatch(3) " + \
                "select symbol, price, volume " + \
                "insert into OutputStream; "

        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query)

        _self_shaddow = self
        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        executionPlanRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = executionPlanRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = executionPlanRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)


        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                log.info("Query: " + queryName + ":" + queryTerminal.name)
                log.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if count == 1:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),"Incorrect debug event received at IN")
                elif count == 2:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),"Incorrect debug event received at IN")
                elif count == 3:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 60.0, 50], event.getOutputData(),
                                                  "Incorrect debug event received at IN")

                debugger.play()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])
        inputHandler.send(["WSO2", 60.0, 50])


        sleep(0.1)

        self.assertEquals(3, self.inEventCount.get(),"Invalid number of output events")
        self.assertEquals(3, self.debugEventCount.get(),"Invalid number of debug events")


        executionPlanRuntime.shutdown()
        siddhiManager.shutdown()


    def test_debugger7(self):
        logging.info("Siddi Debugger Test 7: Test play traversal in a query with time batch window")

        siddhiManager = SiddhiManager()

        cseEventStream = "define stream cseEventStream (symbol string, price float, volume int);";
        query =  "@info(name = 'query1')" + \
                "from cseEventStream#window.timeBatch(3 sec) " + \
                "select symbol, price, volume " + \
                "insert into OutputStream; "

        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query)

        _self_shaddow = self
        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        executionPlanRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = executionPlanRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = executionPlanRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        current_milli_time = lambda: int(round(time.time() * 1000))

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):

                log.info("Query: " + queryName + "\t" + str(current_milli_time()))
                log.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if count == 1:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),"Incorrect debug event received at IN")
                elif count == 2:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),"Incorrect debug event received at IN")
                elif count == 3:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 60.0, 50], event.getOutputData(),
                                                  "Incorrect debug event received at IN")

                debugger.play()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])
        inputHandler.send(["WSO2", 60.0, 50])


        sleep(3.5)

        self.assertEquals(3, self.inEventCount.get(),"Invalid number of output events")
        self.assertEquals(3, self.debugEventCount.get(),"Invalid number of debug events")


        executionPlanRuntime.shutdown()
        siddhiManager.shutdown()


    def test_debugger8(self):
        logging.info("Siddi Debugger Test 8: Test play traversal in a query with time batch window where play call delays" + \
                " 1 sec")

        siddhiManager = SiddhiManager()

        cseEventStream = "define stream cseEventStream (symbol string, price float, volume int);"
        query =  "@info(name = 'query1')" + \
                "from cseEventStream#window.timeBatch(1 sec) " + \
                "select symbol, price, volume " + \
                "insert into OutputStream; "

        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query)

        _self_shaddow = self
        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        executionPlanRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = executionPlanRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = executionPlanRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        current_milli_time = lambda: int(round(time.time() * 1000))

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):

                log.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                _self_shaddow.assertEquals(1, _self_shaddow.getCount(event),"Only one event can be emitted from the window")

                if count != 1 and "query1IN" == queryName :
                    sleep(1)

                debugger.play()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])
        inputHandler.send(["WSO2", 60.0, 50])


        sleep(1.5)

        self.assertEquals(3, self.inEventCount.get(),"Invalid number of output events")
        self.assertEquals(3, self.debugEventCount.get(),"Invalid number of debug events")


        executionPlanRuntime.shutdown()
        siddhiManager.shutdown()


    def test_debugger10(self):
        logging.info("Siddi Debugger Test 10: Test next traversal in a query with two consequent streams")

        siddhiManager = SiddhiManager()

        cseEventStream = "@config(async = 'true') " + \
                "define stream cseEventStream (symbol string, price float, volume int); " + \
                "define stream stockEventStream (symbol string, price float, volume int); "

        query =  "@info(name = 'query1')" + \
                "from cseEventStream " + \
                "select symbol, price, volume " + \
                "insert into stockEventStream; " + \
                "@info(name = 'query2')" + \
                "from stockEventStream " + \
                "select * " + \
                "insert into OutputStream;"


        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query)

        _self_shaddow = self
        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        executionPlanRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = executionPlanRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = executionPlanRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        current_milli_time = lambda: int(round(time.time() * 1000))

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                log.info("Query: " + queryName + ":" + queryTerminal.name)
                log.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))
                if 1 <= count <= 4:
                    # First four events
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),"Incorrect debug event received")
                else:
                    #Next four events
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),"Incorrect debug event received")

                if (count == 1 or count == 5) :
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                elif (count == 2 or count == 6):
                    _self_shaddow.assertEquals("query1OUT", queryName + queryTerminal.name,"Incorrect break point")
                elif (count == 3 or count == 7):
                    _self_shaddow.assertEquals("query2IN", queryName + queryTerminal.name,"Incorrect break point")
                else:
                    _self_shaddow.assertEquals("query2OUT", queryName + queryTerminal.name, "Incorrect break point")


                debugger.next()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])


        sleep(0.1)

        self.assertEquals(2, self.inEventCount.get(),"Invalid number of output events")
        self.assertEquals(8, self.debugEventCount.get(),"Invalid number of debug events")


        executionPlanRuntime.shutdown()
        siddhiManager.shutdown()


    def test_debugger11(self):
        logging.info("Siddi Debugger Test 11: Modify events during debug mode")

        siddhiManager = SiddhiManager()

        cseEventStream = "@config(async = 'true') " + \
                "define stream cseEventStream (symbol string, price float, volume int); " + \
                "define stream stockEventStream (symbol string, price float, volume int); "

        query =  "@info(name = 'query1')" + \
                "from cseEventStream " + \
                "select symbol, price, volume " + \
                "insert into stockEventStream; " + \
                "@info(name = 'query2')" + \
                "from stockEventStream " + \
                "select * " + \
                "insert into OutputStream;"


        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query)

        _self_shaddow = self
        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        executionPlanRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = executionPlanRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = executionPlanRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        current_milli_time = lambda: int(round(time.time() * 1000))

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                log.info("Query: " + queryName + ":" + queryTerminal.name)
                log.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if (count == 1 or count == 2):
                    #WSO2 in stream 1
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),"Incorrect debug event received")
                else:
                    # IBM in stream 2
                    _self_shaddow.assertListEqual(["IBM", 50.0, 60], event.getOutputData(),"Incorrect debug event received")


                if count == 2:
                    #Modify the event at the end of the first stream
                    event.getOutputData()[0] = "IBM"

                debugger.next()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])


        sleep(0.1)

        self.assertEquals(1, self.inEventCount.get(),"Invalid number of output events")
        self.assertEquals(4, self.debugEventCount.get(),"Invalid number of debug events")


        executionPlanRuntime.shutdown()
        siddhiManager.shutdown()


#t = TestDebugger()
#t.setUp()
#t.test_debugger4()

if __name__ == '__main__':
    unittest.main()

#TODO: Fix issue with test 4
#TODO: Add Test 9
#TODO: Test 11: For this test to pass, should implement write backs
#TODO: Test 12