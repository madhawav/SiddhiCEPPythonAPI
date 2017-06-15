package org.wso2.siddhi.pythonapi.event_polling;

/**
 * Created by madhawa on 6/15/17.
 */
public class InstanceManager {
    // A non static class InstanceManager is needed to obtain singleton of EventQueue since pyjnius doesnt support static methods
    private static EventQueue eventQueue = null;
    public EventQueue getEventQueueInstance(){
        if(InstanceManager.eventQueue == null)
        {
            InstanceManager.eventQueue = new EventQueue();
        }
        return InstanceManager.eventQueue;
    }
}
