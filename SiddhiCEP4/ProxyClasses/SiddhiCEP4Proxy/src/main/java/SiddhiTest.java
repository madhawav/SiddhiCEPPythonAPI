import org.apache.log4j.Logger;
import org.wso2.siddhi.core.SiddhiAppRuntime;
import org.wso2.siddhi.core.SiddhiManager;
import org.wso2.siddhi.core.debugger.SiddhiDebugger;
import org.wso2.siddhi.core.debugger.SiddhiDebuggerCallback;
import org.wso2.siddhi.core.event.ComplexEvent;
import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.core.event.stream.StreamEvent;
import org.wso2.siddhi.core.query.output.callback.QueryCallback;
import org.wso2.siddhi.core.stream.input.InputHandler;
import org.wso2.siddhi.core.stream.output.StreamCallback;
import org.wso2.siddhi.core.util.EventPrinter;
import org.wso2.siddhi.core.util.SiddhiTestHelper;

import java.util.Map;
import java.util.concurrent.Semaphore;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Created by madhawa on 5/27/17.
 */
public class SiddhiTest {
    private static final Logger log = Logger.getLogger(SiddhiTest.class);
    private static volatile int count;
    private AtomicInteger inEventCount = new AtomicInteger(0);
    private AtomicInteger debugEventCount = new AtomicInteger(0);

    public void doTest1(){
        SiddhiManager siddhiManager = new SiddhiManager();

        String cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, " +
                "volume int);";
        final String query = "@info(name = 'query 1')" +
                "from cseEventStream " +
                "select symbol, price, volume " +
                "insert into OutputStream; ";

        SiddhiAppRuntime siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query);

        siddhiAppRuntime.addCallback("OutputStream", new StreamCallback() {
            @Override
            public void receive(Event[] events) {
                inEventCount.addAndGet(events.length);
            }
        });
        InputHandler inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream");

        SiddhiDebugger siddhiDebugger = siddhiAppRuntime.debug();
        siddhiDebugger.acquireBreakPoint("query 1", SiddhiDebugger.QueryTerminal.IN);

        siddhiDebugger.setDebuggerCallback(new SiddhiDebuggerCallback() {
            public void debugEvent(ComplexEvent event, String queryName, SiddhiDebugger.QueryTerminal queryTerminal,
                                   SiddhiDebugger debugger) {
                log.info("Query: " + queryName + ":" + queryTerminal);
                log.info(event);

                debugger.next();
            }
        });

        try {
            inputHandler.send(new Object[]{"WSO2", 50f, 60});
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        try {
            inputHandler.send(new Object[]{"WSO2", 70f, 40});
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }


        siddhiAppRuntime.shutdown();
    }


    public void init() {
        inEventCount.set(0);
        debugEventCount.set(0);
    }

    private int getCount(ComplexEvent event) {
        int count = 0;
        while (event != null) {
            count++;
            event = event.getNext();
        }

        return count;
    }

    public void testDebugger4() throws InterruptedException {
        log.info("Siddi Debugger Test 4: Test next traversal in a query with time batch window where next call delays" +
                " 1 sec");

        SiddhiManager siddhiManager = new SiddhiManager();

        String cseEventStream = "define stream cseEventStream (symbol string, price float, volume int);";
        final String query = "@info(name = 'query1')" +
                "from cseEventStream#window.timeBatch(1 sec) " +
                "select symbol, price, volume " +
                "insert into OutputStream; ";

        SiddhiAppRuntime siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query);

        siddhiAppRuntime.addCallback("OutputStream", new StreamCallback() {
            @Override
            public void receive(Event[] events) {
                inEventCount.addAndGet(events.length);
                //Assert.assertEquals("Cannot emit all three in one time", 1, events.length);
            }
        });
        InputHandler inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream");

        SiddhiDebugger siddhiDebugger = siddhiAppRuntime.debug();
        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN);

        siddhiDebugger.setDebuggerCallback(new SiddhiDebuggerCallback() {
            public void debugEvent(ComplexEvent event, String queryName, SiddhiDebugger.QueryTerminal queryTerminal,
                                   SiddhiDebugger debugger) {
                log.info(event);

                int count = debugEventCount.addAndGet(getCount(event));

                if (count != 1 && queryTerminal == SiddhiDebugger.QueryTerminal.IN) {
                    try {
                        Thread.sleep(1100);
                    } catch (InterruptedException e) {
                    }
                }
                // next call will not reach OUT since there is a window
                debugger.next();
            }


        });

        inputHandler.send(new Object[]{"WSO2", 50f, 60});
        inputHandler.send(new Object[]{"WSO2", 70f, 40});
        inputHandler.send(new Object[]{"WSO2", 60f, 50});

        Thread.sleep(1500);

        if(inEventCount.get() != 3)
            log.fatal("Invalid number of output events " + inEventCount.get());

        if(debugEventCount.get() != 3)
            log.fatal("Invalid number of debug events " + debugEventCount.get());


        siddhiAppRuntime.shutdown();
    }


    public void testDebugger9() throws InterruptedException {
        log.info("Siddi Debugger Test 9: Test state traversal in a simple query");

        SiddhiManager siddhiManager = new SiddhiManager();

        String cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, " +
                "volume int);";
        final String query = "@info(name = 'query1')" +
                "from cseEventStream#window.length(3) " +
                "select symbol, price, sum(volume) as volume " +
                "insert into OutputStream; ";

        SiddhiAppRuntime siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query);

        siddhiAppRuntime.addCallback("OutputStream", new StreamCallback() {
            @Override
            public void receive(Event[] events) {
                inEventCount.addAndGet(events.length);
            }
        });
        InputHandler inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream");

        SiddhiDebugger siddhiDebugger = siddhiAppRuntime.debug();
        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN);

        siddhiDebugger.setDebuggerCallback(new SiddhiDebuggerCallback() {
            public void debugEvent(ComplexEvent event, String queryName, SiddhiDebugger.QueryTerminal queryTerminal,
                                   SiddhiDebugger debugger) {
                log.info("Query: " + queryName + ":" + queryTerminal);
                log.info(event);

                int count = debugEventCount.addAndGet(getCount(event));
                if (count == 2) {
                    Map<String, Object> queryState = debugger.getQueryState(queryName);
                    log.info(queryState);
                    log.info(queryState.values().toArray()[0]);
                    StreamEvent streamEvent = null;

                    // Order of the query state items is unpredictable
                    for (Map.Entry<String, Object> entry : queryState.entrySet()) {
                        if (entry.getKey().startsWith("AbstractStreamProcessor")) {
                            streamEvent = (StreamEvent) ((Map<String, Object>) entry.getValue()).get
                                    ("ExpiredEventChunk");
                            break;
                        }
                    }
                    //Assert.assertArrayEquals(streamEvent.getOutputData(), new Object[]{"WSO2", 50.0f, null});
                }
                debugger.next();
            }
        });
        inputHandler.send(new Object[]{"WSO2", 50f, 60});
        inputHandler.send(new Object[]{"WSO2", 70f, 40});

        Thread.sleep(100);

        //Assert.assertEquals("Invalid number of output events", 2, inEventCount.get());
        //Assert.assertEquals("Invalid number of debug events", 4, debugEventCount.get());

        siddhiAppRuntime.shutdown();
    }

    public void testExtension() throws InterruptedException {
        log.info("ContainsFunctionExtensionTestCase TestCase");
        SiddhiManager siddhiManager = new SiddhiManager();

        String inStreamDefinition = "define stream inputStream (symbol string, price long, " +
                "volume long);";
        String query = ("@info(name = 'query1') " +
                "from inputStream " +
                "select symbol , str:contains(symbol, 'WSO2') as isContains " +
                "insert into outputStream;");
        SiddhiAppRuntime siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(inStreamDefinition +
                query);

        siddhiAppRuntime.addCallback("query1", new QueryCallback() {
            @Override
            public void receive(long timeStamp, Event[] inEvents, Event[] removeEvents) {
                EventPrinter.print(timeStamp, inEvents, removeEvents);
                for (Event inEvent : inEvents) {
                    log.info(inEvent);
                }
            }
        });

        InputHandler inputHandler = siddhiAppRuntime.getInputHandler("inputStream");
        siddhiAppRuntime.start();
        inputHandler.send(new Object[]{"IBM", 700f, 100L});
        inputHandler.send(new Object[]{"WSO2", 60.5f, 200L});
        inputHandler.send(new Object[]{"One of the best middleware is from WSO2.", 60.5f, 200L});
        Thread.sleep(100);
        siddhiAppRuntime.shutdown();
    }
    double betaZero = 0;
    public void simpleRegressionTest() throws InterruptedException {
        log.info("Simple Regression TestCase");

        SiddhiManager siddhiManager = new SiddhiManager();
        siddhiManager.setExtension("timeseries:regress",org.wso2.extension.siddhi.execution.timeseries.LinearRegressionStreamProcessor.class);
        String inputStream = "define stream InputStream (y int, x int);";

        String siddhiApp = ("@info(name = 'query1') from InputStream#timeseries:regress(1, 100, 0.95, y, x) "
                + "select * "
                + "insert into OutputStream;");
        SiddhiAppRuntime siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(inputStream + siddhiApp);

        siddhiAppRuntime.addCallback("query1", new QueryCallback() {
            @Override
            public void receive(long timeStamp, Event[] inEvents,
                                Event[] removeEvents) {
                EventPrinter.print(timeStamp, inEvents, removeEvents);
                count = count + inEvents.length;
                betaZero = (Double) inEvents[inEvents.length - 1].getData(3);
            }
        });
        InputHandler inputHandler = siddhiAppRuntime.getInputHandler("InputStream");
        siddhiAppRuntime.start();

        //system.out.println(System.currentTimeMillis());

        inputHandler.send(new Object[]{2500.00, 17.00});
        inputHandler.send(new Object[]{2600.00, 18.00});
        inputHandler.send(new Object[]{3300.00, 31.00});
        inputHandler.send(new Object[]{2475.00, 12.00});
        inputHandler.send(new Object[]{2313.00, 8.00});
        inputHandler.send(new Object[]{2175.00, 26.00});
        inputHandler.send(new Object[]{600.00, 14.00});
        inputHandler.send(new Object[]{460.00, 3.00});
        inputHandler.send(new Object[]{240.00, 1.00});
        inputHandler.send(new Object[]{200.00, 10.00});
        inputHandler.send(new Object[]{177.00, 0.00});
        inputHandler.send(new Object[]{140.00, 6.00});
        inputHandler.send(new Object[]{117.00, 1.00});
        inputHandler.send(new Object[]{115.00, 0.00});
        inputHandler.send(new Object[]{2600.00, 19.00});
        inputHandler.send(new Object[]{1907.00, 13.00});
        inputHandler.send(new Object[]{1190.00, 3.00});
        inputHandler.send(new Object[]{990.00, 16.00});
        inputHandler.send(new Object[]{925.00, 6.00});
        inputHandler.send(new Object[]{365.00, 0.00});
        inputHandler.send(new Object[]{302.00, 10.00});
        inputHandler.send(new Object[]{300.00, 6.00});
        inputHandler.send(new Object[]{129.00, 2.00});
        inputHandler.send(new Object[]{111.00, 1.00});
        inputHandler.send(new Object[]{6100.00, 18.00});
        inputHandler.send(new Object[]{4125.00, 19.00});
        inputHandler.send(new Object[]{3213.00, 1.00});
        inputHandler.send(new Object[]{2319.00, 38.00});
        inputHandler.send(new Object[]{2000.00, 10.00});
        inputHandler.send(new Object[]{1600.00, 0.00});
        inputHandler.send(new Object[]{1394.00, 4.00});
        inputHandler.send(new Object[]{935.00, 4.00});
        inputHandler.send(new Object[]{850.00, 0.00});
        inputHandler.send(new Object[]{775.00, 5.00});
        inputHandler.send(new Object[]{760.00, 6.00});
        inputHandler.send(new Object[]{629.00, 1.00});
        inputHandler.send(new Object[]{275.00, 6.00});
        inputHandler.send(new Object[]{120.00, 0.00});
        inputHandler.send(new Object[]{2567.00, 12.00});
        inputHandler.send(new Object[]{2500.00, 28.00});
        inputHandler.send(new Object[]{2350.00, 21.00});
        inputHandler.send(new Object[]{2317.00, 3.00});
        inputHandler.send(new Object[]{2000.00, 12.00});
        inputHandler.send(new Object[]{715.00, 1.00});
        inputHandler.send(new Object[]{660.00, 9.00});
        inputHandler.send(new Object[]{650.00, 0.00});
        inputHandler.send(new Object[]{260.00, 0.00});
        inputHandler.send(new Object[]{250.00, 1.00});
        inputHandler.send(new Object[]{200.00, 13.00});
        inputHandler.send(new Object[]{180.00, 6.00});
        Thread.sleep(100);

        siddhiAppRuntime.shutdown();
    }
    public void testSetCallback() throws InterruptedException {
        log.info("Siddi Debugger Test 1: Test next traversal in a simple query");

        SiddhiManager siddhiManager = new SiddhiManager();

        String cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, " +
                "volume int);";
        final String query = "@info(name = 'query 1')" +
                "from cseEventStream " +
                "select symbol, price, volume " +
                "insert into OutputStream; ";

        SiddhiAppRuntime siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query);

        siddhiAppRuntime.addCallback("OutputStream", new StreamCallback() {
            @Override
            public void receive(Event[] events) {
                inEventCount.addAndGet(events.length);
            }
        });
        InputHandler inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream");

        SiddhiDebugger siddhiDebugger = siddhiAppRuntime.debug();
        siddhiDebugger.acquireBreakPoint("query 1", SiddhiDebugger.QueryTerminal.IN);

        siddhiDebugger.setDebuggerCallback(new SiddhiDebuggerCallback() {
            public void debugEvent(ComplexEvent event, String queryName, SiddhiDebugger.QueryTerminal queryTerminal,
                                   SiddhiDebugger debugger) {
                log.info("C1: Query: " + queryName + ":" + queryTerminal);
                log.info(event);

                int count = debugEventCount.addAndGet(getCount(event));
                debugger.next();
            }
        });

        siddhiDebugger.acquireBreakPoint("query 1", SiddhiDebugger.QueryTerminal.IN);

        inputHandler.send(new Object[]{"WSO2", 50f, 60});

        siddhiDebugger.setDebuggerCallback(new SiddhiDebuggerCallback() {
            public void debugEvent(ComplexEvent event, String queryName, SiddhiDebugger.QueryTerminal queryTerminal,
                                   SiddhiDebugger debugger) {
                log.info("C2: Query: " + queryName + ":" + queryTerminal);
                log.info(event);

                int count = debugEventCount.addAndGet(getCount(event));
                debugger.next();
            }
        });

        inputHandler.send(new Object[]{"WSO2", 70f, 40});

        Thread.sleep(100);

        //Assert.assertEquals("Invalid number of output events", 2, inEventCount.get());
        //Assert.assertEquals("Invalid number of debug events", 4, debugEventCount.get());

        siddhiAppRuntime.shutdown();
    }

    public void testAcquireReleaseBreakpoint() throws InterruptedException {
        log.info("Siddi Debugger Test 1: Test next traversal in a simple query");

        SiddhiManager siddhiManager = new SiddhiManager();

        String cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, " +
                "volume int);";
        final String query = "@info(name = 'query 1')" +
                "from cseEventStream " +
                "select symbol, price, volume " +
                "insert into OutputStream; ";

        SiddhiAppRuntime siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query);

        siddhiAppRuntime.addCallback("OutputStream", new StreamCallback() {
            @Override
            public void receive(Event[] events) {
                inEventCount.addAndGet(events.length);
            }
        });
        InputHandler inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream");

        SiddhiDebugger siddhiDebugger = siddhiAppRuntime.debug();
        siddhiDebugger.acquireBreakPoint("query 1", SiddhiDebugger.QueryTerminal.IN);

        siddhiDebugger.setDebuggerCallback(new SiddhiDebuggerCallback() {
            public void debugEvent(ComplexEvent event, String queryName, SiddhiDebugger.QueryTerminal queryTerminal,
                                   SiddhiDebugger debugger) {
                log.info("Query: " + queryName + ":" + queryTerminal);
                log.info(event);

                int count = debugEventCount.addAndGet(getCount(event));
                debugger.play();
            }
        });

        siddhiDebugger.acquireBreakPoint("query 1", SiddhiDebugger.QueryTerminal.IN);

        inputHandler.send(new Object[]{"WSO2", 50f, 60});

        siddhiDebugger.releaseBreakPoint("query 1", SiddhiDebugger.QueryTerminal.IN);

        inputHandler.send(new Object[]{"WSO2", 70f, 40});

        Thread.sleep(100);

        //Assert.assertEquals("Invalid number of output events", 2, inEventCount.get());
        //Assert.assertEquals("Invalid number of debug events", 4, debugEventCount.get());

        siddhiAppRuntime.shutdown();
    }

    public static void main(String[] args) throws InterruptedException {

       SiddhiTest st = new SiddhiTest();
       st.init();
       st.simpleRegressionTest();
    }
}
