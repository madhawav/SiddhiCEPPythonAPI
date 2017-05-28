package org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback;

import org.wso2.siddhi.core.debugger.SiddhiDebugger;
import org.wso2.siddhi.core.event.ComplexEvent;
import org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger.QueryTerminalProxy;

/**
 * Created by madhawa on 5/27/17.
 */
public interface DebugEventCallbackProxy {
    void debugEvent(ComplexEvent complexEvent, String queryName, QueryTerminalProxy queryTerminal, SiddhiDebugger debugger);
    void gc();
}
