package org.wso2.siddhi.pythonapi.event_polling;

import org.wso2.siddhi.core.debugger.SiddhiDebugger;
import org.wso2.siddhi.core.event.ComplexEvent;
import org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger.QueryTerminalProxy;
import org.wso2.siddhi.pythonapi.proxy.core.event.complex_event.ComplexEventProxy;

/**
 * Created by madhawa on 6/15/17.
 */
public class QueuedEvent {
    public enum QueuedEventType{
        DebuggerCallbackEvent
    }

    public static QueuedEvent createDebuggerCallbackEvent(ComplexEvent complexEvent, String queryName, QueryTerminalProxy queryTerminal, SiddhiDebugger debugger)
    {
        Object[] params = {complexEvent, queryName,queryTerminal, debugger};
        return new QueuedEvent(QueuedEventType.DebuggerCallbackEvent,params);
    }

    public QueuedEvent(QueuedEventType eventType, Object[] parameters)
    {
        this.eventType = eventType;
        this.parameters = parameters;
    }

    private QueuedEventType eventType;
    private Object[] parameters;

    public QueuedEventType getEventType(){
        return eventType;
    }

    public boolean isDebuggerCallback(){
        return eventType == QueuedEventType.DebuggerCallbackEvent;
    }

    public ComplexEvent getComplexEvent(int parameterId)
    {
        return (ComplexEvent) parameters[parameterId];
    }

    public String getString(int parameterId)
    {
        return (String) parameters[parameterId];
    }

    public SiddhiDebugger getSiddhiDebugger(int parameterId)
    {
        System.out.println("Get Debugger Requested");
        return (SiddhiDebugger) parameters[parameterId];
    }

    public QueryTerminalProxy getQueryTerminal(int parameterId)
    {
        return (QueryTerminalProxy) parameters[parameterId];
    }
}
