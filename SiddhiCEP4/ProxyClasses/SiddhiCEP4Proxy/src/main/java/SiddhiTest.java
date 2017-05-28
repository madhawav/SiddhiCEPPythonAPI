import org.apache.log4j.Logger;
import org.wso2.siddhi.core.ExecutionPlanRuntime;
import org.wso2.siddhi.core.SiddhiManager;
import org.wso2.siddhi.core.debugger.SiddhiDebugger;
import org.wso2.siddhi.core.debugger.SiddhiDebuggerCallback;
import org.wso2.siddhi.core.event.ComplexEvent;
import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.core.stream.input.InputHandler;
import org.wso2.siddhi.core.stream.output.StreamCallback;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * Created by madhawa on 5/27/17.
 */
public class SiddhiTest {
    private static final Logger log = Logger.getLogger(SiddhiTest.class);
    private static volatile int count;
    private AtomicInteger inEventCount = new AtomicInteger(0);
    private AtomicInteger debugEventCount = new AtomicInteger(0);
    public void doTest(){
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
    public static void main(String[] args) {

       new SiddhiTest().doTest();
    }
}
