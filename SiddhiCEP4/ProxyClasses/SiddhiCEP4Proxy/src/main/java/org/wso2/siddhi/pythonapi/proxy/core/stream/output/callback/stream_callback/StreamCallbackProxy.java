package org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback;

import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.core.stream.output.StreamCallback;

/**
 * Created by madhawa on 5/26/17.
 */
public class StreamCallbackProxy extends StreamCallback {
    private ReceiveCallbackProxy receiveCallback = null;
    public void setReceiveCallback(ReceiveCallbackProxy value){
        this.receiveCallback = value;
    }


    public void receive(Event[] events) {
        this.receiveCallback.receive(events);
    }
}
