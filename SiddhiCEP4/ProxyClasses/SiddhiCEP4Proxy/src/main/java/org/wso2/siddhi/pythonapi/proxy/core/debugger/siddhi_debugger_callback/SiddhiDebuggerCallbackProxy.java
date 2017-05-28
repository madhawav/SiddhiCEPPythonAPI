package org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback;

import org.apache.log4j.Logger;
import org.wso2.siddhi.core.debugger.SiddhiDebugger;
import org.wso2.siddhi.core.debugger.SiddhiDebuggerCallback;
import org.wso2.siddhi.core.event.ComplexEvent;
import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger.QueryTerminalProxy;
import org.wso2.siddhi.pythonapi.proxy.core.query.output.callback.query_callback.ReceiveCallbackProxy;
import org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy;

/**
 * Created by madhawa on 5/27/17.
 */
public class SiddhiDebuggerCallbackProxy implements SiddhiDebuggerCallback {
    private DebugEventCallbackProxy debugEventCallback = null;
    public void setDebugEventCallback(DebugEventCallbackProxy value){
        this.debugEventCallback = value;
    }

    private static final Logger log = Logger.getLogger(StreamCallbackProxy.class);

    public void debugEvent(ComplexEvent complexEvent, String queryName, SiddhiDebugger.QueryTerminal queryTerminal, SiddhiDebugger siddhiDebugger) {
        this.debugEventCallback.debugEvent(complexEvent,queryName,new QueryTerminalProxy(queryTerminal), siddhiDebugger);
    }

    @Override
    public void finalize() throws java.lang.Throwable {
        //We need to inform Python when Java GC collects so it can remove the references held
        log.info("Java GC Collection");
        this.debugEventCallback.gc();
    }
}
