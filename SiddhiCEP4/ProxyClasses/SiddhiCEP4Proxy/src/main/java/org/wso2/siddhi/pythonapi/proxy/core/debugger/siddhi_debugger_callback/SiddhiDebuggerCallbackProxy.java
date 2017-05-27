package org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback;

import org.wso2.siddhi.core.debugger.SiddhiDebugger;
import org.wso2.siddhi.core.debugger.SiddhiDebuggerCallback;
import org.wso2.siddhi.core.event.ComplexEvent;
import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger.QueryTerminalProxy;
import org.wso2.siddhi.pythonapi.proxy.core.query.output.callback.query_callback.ReceiveCallbackProxy;

/**
 * Created by madhawa on 5/27/17.
 */
public class SiddhiDebuggerCallbackProxy implements SiddhiDebuggerCallback {
    private DebugEventCallbackProxy debugEventCallback = null;
    public void setDebugEventCallback(DebugEventCallbackProxy value){
        this.debugEventCallback = value;
    }


    public void debugEvent(ComplexEvent complexEvent, String queryName, SiddhiDebugger.QueryTerminal queryTerminal, SiddhiDebugger siddhiDebugger) {
        this.debugEventCallback.debugEvent(complexEvent,queryName,new QueryTerminalProxy(queryTerminal), siddhiDebugger);
    }
}
