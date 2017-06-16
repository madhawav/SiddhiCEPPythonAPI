package org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback.event_polling;

import org.apache.log4j.Logger;
import org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy;

import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 * Shared Queue of events between Java and Python. Used to pass Debug Events to Python from Java using polling.
 */
public class EventQueue {
    private Queue<QueuedEvent> queuedEvents = null;

    /**
     * Instantiate a new EventQueue
     */
    public EventQueue(){
        this.queuedEvents = new ConcurrentLinkedQueue<QueuedEvent>();
    }

    private static final Logger log = Logger.getLogger(EventQueue.class);

    /**
     * Retrieve the next event in queue. Returns null if queue is empty.
     * @return
     */
    public QueuedEvent getQueuedEvent(){
        if(queuedEvents.isEmpty())
            return null;
        return queuedEvents.remove();
    }

    /**
     * Adds an event to event queue.
     * @param event Event to be added
     */
    public void addEvent(QueuedEvent event)
    {
        log.trace("Event Added");
        queuedEvents.add(event);
    }
}

