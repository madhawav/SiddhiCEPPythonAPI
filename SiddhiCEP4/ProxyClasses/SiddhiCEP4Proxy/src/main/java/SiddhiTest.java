import org.apache.log4j.Logger;
import org.wso2.siddhi.core.ExecutionPlanRuntime;
import org.wso2.siddhi.core.SiddhiManager;
import org.wso2.siddhi.core.debugger.SiddhiDebugger;
import org.wso2.siddhi.core.debugger.SiddhiDebuggerCallback;
import org.wso2.siddhi.core.event.ComplexEvent;
import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.core.event.stream.StreamEvent;
import org.wso2.siddhi.core.stream.input.InputHandler;
import org.wso2.siddhi.core.stream.output.StreamCallback;

import java.util.Map;
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

        ExecutionPlanRuntime executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query);

        executionPlanRuntime.addCallback("OutputStream", new StreamCallback() {
            @Override
            public void receive(Event[] events) {
                inEventCount.addAndGet(events.length);
            }
        });
        InputHandler inputHandler = executionPlanRuntime.getInputHandler("cseEventStream");

        SiddhiDebugger siddhiDebugger = executionPlanRuntime.debug();
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


        executionPlanRuntime.shutdown();
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

        ExecutionPlanRuntime executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query);

        executionPlanRuntime.addCallback("OutputStream", new StreamCallback() {
            @Override
            public void receive(Event[] events) {
                inEventCount.addAndGet(events.length);
                //Assert.assertEquals("Cannot emit all three in one time", 1, events.length);
            }
        });
        InputHandler inputHandler = executionPlanRuntime.getInputHandler("cseEventStream");

        SiddhiDebugger siddhiDebugger = executionPlanRuntime.debug();
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


        executionPlanRuntime.shutdown();
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

        ExecutionPlanRuntime executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query);

        executionPlanRuntime.addCallback("OutputStream", new StreamCallback() {
            @Override
            public void receive(Event[] events) {
                inEventCount.addAndGet(events.length);
            }
        });
        InputHandler inputHandler = executionPlanRuntime.getInputHandler("cseEventStream");

        SiddhiDebugger siddhiDebugger = executionPlanRuntime.debug();
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

        executionPlanRuntime.shutdown();
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

        ExecutionPlanRuntime executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query);

        executionPlanRuntime.addCallback("OutputStream", new StreamCallback() {
            @Override
            public void receive(Event[] events) {
                inEventCount.addAndGet(events.length);
            }
        });
        InputHandler inputHandler = executionPlanRuntime.getInputHandler("cseEventStream");

        SiddhiDebugger siddhiDebugger = executionPlanRuntime.debug();
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

        executionPlanRuntime.shutdown();
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

        ExecutionPlanRuntime executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(cseEventStream + query);

        executionPlanRuntime.addCallback("OutputStream", new StreamCallback() {
            @Override
            public void receive(Event[] events) {
                inEventCount.addAndGet(events.length);
            }
        });
        InputHandler inputHandler = executionPlanRuntime.getInputHandler("cseEventStream");

        SiddhiDebugger siddhiDebugger = executionPlanRuntime.debug();
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

        executionPlanRuntime.shutdown();
    }

    public static void main(String[] args) throws InterruptedException {

       SiddhiTest st = new SiddhiTest();
       st.init();
       st.testSetCallback();
    }
}
