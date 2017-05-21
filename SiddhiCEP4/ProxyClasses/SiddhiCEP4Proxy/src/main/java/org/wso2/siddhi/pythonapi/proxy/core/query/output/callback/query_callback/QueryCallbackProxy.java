package org.wso2.siddhi.pythonapi.proxy.core.query.output.callback.query_callback;

import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.core.query.output.callback.QueryCallback;

/**
 * Created by madhawa on 5/21/17.
 */
public class QueryCallbackProxy extends QueryCallback {
    private ReceiveCallbackProxy receiveCallback = null;
    public void setReceiveCallback(ReceiveCallbackProxy value){
        this.receiveCallback = value;
    }

    public void receive(long timestamp, Event[] inEvents, Event[] ouEvents) {
        this.receiveCallback.receive(timestamp,inEvents,ouEvents);
    }
}
