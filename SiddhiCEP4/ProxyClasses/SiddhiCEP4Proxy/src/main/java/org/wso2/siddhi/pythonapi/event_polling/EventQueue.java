package org.wso2.siddhi.pythonapi.event_polling;

import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 * Created by madhawa on 6/15/17.
 */
public class EventQueue {
    private Queue<QueuedEvent> queuedEvents = null;
    EventQueue(){
        this.queuedEvents = new ConcurrentLinkedQueue<QueuedEvent>();
    }
    public QueuedEvent getQueuedEvent(){
        if(queuedEvents.isEmpty())
            return null;
        return queuedEvents.remove();
    }

    public void addEvent(QueuedEvent event)
    {
        System.out.println("Event added");
        queuedEvents.add(event);
    }
}

